import cv2
import mediapipe as mp

from config import (
    EAR_THRESHOLD,
    CALIBRATION_FRAMES,
    CALIBRATION_FACTOR,
    validate_config
)

from core.gestures import BlinkGesture
from core.eye_tracker import EyeTracker
from core.calibration import EyeCalibration
from core.pattern_buffer import PatternBuffer


mp_face_mesh = mp.solutions.face_mesh


def main():

    try:
        validate_config()

    except ValueError as e:

        print(f"[!] Invalid config: {e}")

        return

    blink = BlinkGesture()

    tracker = EyeTracker()

    calibration = EyeCalibration()

    buffer = PatternBuffer()

    current_threshold = EAR_THRESHOLD

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print(
            "[!] Could not open the camera. Check that it's "
            "connected and not in use by another application."
        )

        return

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as face_mesh:

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)

            h, w = frame.shape[:2]

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = face_mesh.process(rgb)

            avg_ear = 0
            status = "NO FACE - move into frame"

            if results.multi_face_landmarks:

                landmarks = (
                    results
                    .multi_face_landmarks[0]
                    .landmark
                )

                avg_ear = tracker.get_avg_ear(
                    landmarks,
                    w,
                    h
                )

                if not calibration.is_calibrated():

                    calibration.update(
                        avg_ear,
                        CALIBRATION_FRAMES,
                        CALIBRATION_FACTOR
                    )

                    status = (
                        f"CALIBRATING "
                        f"({len(calibration.samples)}/"
                        f"{CALIBRATION_FRAMES})"
                    )

                    if calibration.is_calibrated():

                        current_threshold = (
                            calibration.get_threshold()
                        )

                        print(
                            "\n[+] Calibration Complete"
                        )

                        print(
                            f"[+] Threshold = "
                            f"{current_threshold:.3f}\n"
                        )

                else:

                    is_blink = (
                        avg_ear < current_threshold
                    )

                    gesture = blink.update(
                        is_blink
                    )

                    if gesture == "BLINK":

                        buffer.add("B")

                        print(
                            f"BLINK | "
                            f"Total: {blink.count}"
                        )

                    elif gesture == "LONG_BLINK":

                        buffer.add("L")

                        print(
                            f"LONG BLINK | "
                            f"Total: {blink.count}"
                        )

                    status = (
                        "BLINK"
                        if is_blink
                        else "OPEN"
                    )

            else:

                # Face tracking lost mid-blink: clear any in-progress
                # blink state so the tracking gap doesn't get counted
                # toward blink duration once the face reappears.
                blink.reset()

            pattern = buffer.get_pattern()

            if pattern:

                print(
                    f"Pattern: "
                    f"{''.join(pattern)}"
                )

            cv2.putText(
                frame,
                f"EAR: {avg_ear:.2f}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Blinks: {blink.count}",
                (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                status,
                (30, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (
                    (0, 0, 255)
                    if status == "BLINK"
                    else (0, 255, 0)
                ),
                2
            )

            cv2.putText(
                frame,
                f"Threshold: {current_threshold:.2f}",
                (30, 170),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Press 'r' to recalibrate",
                (30, 210),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 200),
                1
            )

            cv2.imshow(
                "Eye-To-Speak",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord("r"):

                calibration.reset()

                blink.reset()

                current_threshold = EAR_THRESHOLD

                print(
                    "\n[+] Recalibration requested — "
                    "hold still with eyes open.\n"
                )

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

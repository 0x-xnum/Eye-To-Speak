import cv2
import mediapipe as mp

from config import EAR_THRESHOLD
from core.gestures import BlinkGesture
from core.eye_tracker import EyeTracker


mp_face_mesh = mp.solutions.face_mesh


def main():

    blink = BlinkGesture()
    tracker = EyeTracker()

    cap = cv2.VideoCapture(0)

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
            status = "NO FACE"

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

                is_blink = (
                    avg_ear < EAR_THRESHOLD
                )

                gesture = blink.update(
                    is_blink
                )

                if gesture:
                    print(
                        f"{gesture} | Total: {blink.count}"
                    )

                status = (
                    "BLINK"
                    if is_blink
                    else "OPEN"
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

            cv2.imshow(
                "Eye-To-Speak",
                frame
            )

            if (
                cv2.waitKey(1)
                & 0xFF
                == ord("q")
            ):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

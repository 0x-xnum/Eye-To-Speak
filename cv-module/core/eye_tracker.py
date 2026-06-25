import numpy as np


LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]


class EyeTracker:

    def eye_aspect_ratio(
        self,
        landmarks,
        eye_indices,
        img_w,
        img_h
    ):

        points = [
            (
                int(landmarks[i].x * img_w),
                int(landmarks[i].y * img_h)
            )
            for i in eye_indices
        ]

        A = np.linalg.norm(
            np.array(points[1]) -
            np.array(points[5])
        )

        B = np.linalg.norm(
            np.array(points[2]) -
            np.array(points[4])
        )

        C = np.linalg.norm(
            np.array(points[0]) -
            np.array(points[3])
        )

        return (A + B) / (2.0 * C)

    def get_avg_ear(
        self,
        landmarks,
        img_w,
        img_h
    ):

        left_ear = self.eye_aspect_ratio(
            landmarks,
            LEFT_EYE,
            img_w,
            img_h
        )

        right_ear = self.eye_aspect_ratio(
            landmarks,
            RIGHT_EYE,
            img_w,
            img_h
        )

        return (
            left_ear + right_ear
        ) / 2

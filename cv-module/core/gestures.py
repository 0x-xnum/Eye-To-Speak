import time

from config import (
    BLINK_COOLDOWN,
    LONG_BLINK_THRESHOLD
)


class BlinkGesture:

    def __init__(self):

        self.count = 0
        self.detected = False
        self.last_blink = 0
        self.blink_start = None

    def update(
        self,
        is_blink
    ):

        now = time.time()

        if is_blink:

            if not self.detected:

                self.detected = True
                self.blink_start = now

            return None

        if self.detected:

            duration = (
                now - self.blink_start
            )

            self.detected = False

            if (
                now - self.last_blink
                < BLINK_COOLDOWN
            ):
                return None

            self.last_blink = now
            self.count += 1

            if (
                duration >=
                LONG_BLINK_THRESHOLD
            ):
                return "LONG_BLINK"

            return "BLINK"

        return None

    def reset(self):
        """
        Clears any in-progress blink state without touching the
        running count. Call this when face tracking is lost
        mid-blink so a gap in tracking (not an actual long eye
        closure) doesn't get misread as a LONG_BLINK once the face
        reappears.
        """

        self.detected = False
        self.blink_start = None

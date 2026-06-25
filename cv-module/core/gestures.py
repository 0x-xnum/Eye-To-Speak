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
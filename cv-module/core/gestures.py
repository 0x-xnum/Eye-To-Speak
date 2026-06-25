import time
from config import BLINK_COOLDOWN


class BlinkGesture:
    def __init__(self):
        self.count = 0
        self.detected = False
        self.last_blink = 0


    def update(self, is_blink):

        if is_blink:
            now = time.time()

            if (
                not self.detected
                and now - self.last_blink > BLINK_COOLDOWN
            ):
                self.count += 1
                self.last_blink = now
                self.detected = True

                return "BLINK"

        else:
            self.detected = False


        return None

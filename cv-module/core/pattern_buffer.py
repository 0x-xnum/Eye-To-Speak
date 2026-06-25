import time


class PatternBuffer:

    def __init__(self):

        self.pattern = []

        self.last_event = time.time()

        self.timeout = 2

    def add(self, gesture):

        self.pattern.append(gesture)

        self.last_event = time.time()

    def get_pattern(self):

        now = time.time()

        if (
            self.pattern
            and now - self.last_event > self.timeout
        ):

            pattern = self.pattern.copy()

            self.pattern.clear()

            return pattern

        return None

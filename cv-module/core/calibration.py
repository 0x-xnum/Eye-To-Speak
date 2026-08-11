class DynamicCalibrator:

    def __init__(self, alpha=0.01):
        self.samples = []
        self.calibrated = False
        self.baseline_ear = None
        self.threshold = None
        self.alpha = alpha  # Learning rate for EMA

    def update(
        self,
        ear,
        max_samples,
        factor
    ):

        # 1. Initial Static Calibration (First 100 frames)
        if not self.calibrated:
            self.samples.append(ear)
            if len(self.samples) >= max_samples:
                self.baseline_ear = sum(self.samples) / len(self.samples)
                self.threshold = self.baseline_ear * factor
                self.calibrated = True
            return

        # 2. Continuous ML Calibration (EMA)
        # Only update the baseline if the eye is OPEN (not mid-blink)
        if ear >= self.threshold:
            # Shift baseline slowly towards the current EAR
            self.baseline_ear = (self.alpha * ear) + ((1.0 - self.alpha) * self.baseline_ear)
            self.threshold = self.baseline_ear * factor

    def get_threshold(self):
        return self.threshold

    def is_calibrated(self):
        return self.calibrated

    def reset(self):
        self.samples = []
        self.calibrated = False
        self.baseline_ear = None
        self.threshold = None

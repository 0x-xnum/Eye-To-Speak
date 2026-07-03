class EyeCalibration:

    def __init__(self):
        self.samples = []
        self.calibrated = False
        self.threshold = None

    def update(
        self,
        ear,
        max_samples,
        factor
    ):

        if self.calibrated:
            return

        self.samples.append(ear)

        if len(self.samples) >= max_samples:

            avg_open_ear = (
                sum(self.samples)
                / len(self.samples)
            )

            self.threshold = (
                avg_open_ear * factor
            )

            self.calibrated = True

    def get_threshold(self):

        return self.threshold

    def is_calibrated(self):

        return self.calibrated

    def reset(self):
        """
        Clears calibration so the next frames are re-sampled from
        scratch. Call this when lighting or camera position changes
        enough that the old threshold no longer fits.
        """

        self.samples = []
        self.calibrated = False
        self.threshold = None

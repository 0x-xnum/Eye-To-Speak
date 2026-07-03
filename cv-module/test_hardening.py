"""
Tests for the hardening additions: config validation, BlinkGesture
reset(), and EyeCalibration reset().
"""

import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))

import config
from core.gestures import BlinkGesture
from core.calibration import EyeCalibration


class TestValidateConfig(unittest.TestCase):

    def test_current_config_is_valid(self):
        # should not raise
        config.validate_config()

    def test_rejects_zero_ear_threshold(self):
        original = config.EAR_THRESHOLD
        config.EAR_THRESHOLD = 0
        try:
            with self.assertRaises(ValueError):
                config.validate_config()
        finally:
            config.EAR_THRESHOLD = original

    def test_rejects_calibration_factor_out_of_range(self):
        original = config.CALIBRATION_FACTOR
        config.CALIBRATION_FACTOR = 1.5
        try:
            with self.assertRaises(ValueError):
                config.validate_config()
        finally:
            config.CALIBRATION_FACTOR = original

    def test_rejects_zero_calibration_frames(self):
        original = config.CALIBRATION_FRAMES
        config.CALIBRATION_FRAMES = 0
        try:
            with self.assertRaises(ValueError):
                config.validate_config()
        finally:
            config.CALIBRATION_FRAMES = original

    def test_rejects_long_blink_threshold_below_cooldown(self):
        original = config.LONG_BLINK_THRESHOLD
        config.LONG_BLINK_THRESHOLD = 0.01
        try:
            with self.assertRaises(ValueError):
                config.validate_config()
        finally:
            config.LONG_BLINK_THRESHOLD = original


class TestBlinkGestureReset(unittest.TestCase):

    def test_reset_clears_in_progress_blink_without_losing_count(self):
        g = BlinkGesture()
        g.count = 5

        with patch("core.gestures.time.time", return_value=100.0):
            g.update(True)  # eyes close, blink in progress

        self.assertTrue(g.detected)

        g.reset()

        self.assertFalse(g.detected)
        self.assertIsNone(g.blink_start)
        self.assertEqual(g.count, 5)  # count untouched

    def test_tracking_gap_does_not_become_long_blink_after_reset(self):
        g = BlinkGesture()

        with patch("core.gestures.time.time", return_value=100.0):
            g.update(True)  # eyes close

        # simulate face tracking lost for a long gap
        g.reset()

        with patch("core.gestures.time.time", return_value=200.0):
            g.update(True)  # eyes closed again once tracking resumes

        with patch("core.gestures.time.time", return_value=200.2):
            result = g.update(False)  # short real blink after resume

        self.assertEqual(result, "BLINK")


class TestEyeCalibrationReset(unittest.TestCase):

    def test_reset_clears_calibration_state(self):
        c = EyeCalibration()

        for _ in range(5):
            c.update(0.3, max_samples=5, factor=0.75)

        self.assertTrue(c.is_calibrated())

        c.reset()

        self.assertFalse(c.is_calibrated())
        self.assertEqual(c.samples, [])
        self.assertIsNone(c.get_threshold())


if __name__ == "__main__":
    unittest.main(verbosity=2)

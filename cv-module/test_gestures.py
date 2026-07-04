"""
Quick sanity test for BlinkGesture with the updated
LONG_BLINK_THRESHOLD (1.0 -> 0.5).

Simulates eye-closed durations without needing a webcam by
patching time.time().
"""

import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))

from core.gestures import BlinkGesture
import config


def simulate_blink(gesture, duration, cooldown_gap=1.0, start_time=1000.0):
    """
    Simulates: eyes close at start_time, stay closed for `duration`
    seconds, then open. Returns whatever `update()` returns on the
    closing-to-open transition.
    """
    with patch("core.gestures.time.time", return_value=start_time):
        gesture.update(True)  # eyes close

    with patch(
        "core.gestures.time.time",
        return_value=start_time + duration,
    ):
        result = gesture.update(False)  # eyes open -> gesture emitted

    with patch(
        "core.gestures.time.time",
        return_value=start_time + duration + cooldown_gap,
    ):
        pass

    return result


class TestBlinkThreshold(unittest.TestCase):

    def test_short_blink_is_normal_blink(self):
        g = BlinkGesture()
        result = simulate_blink(g, duration=0.15)
        self.assertEqual(result, "BLINK")

    def test_previously_normal_now_long_blink(self):
        g = BlinkGesture()
        result = simulate_blink(g, duration=0.6)
        self.assertEqual(result, "LONG_BLINK")

    def test_definite_long_blink_still_long(self):
        g = BlinkGesture()
        result = simulate_blink(g, duration=1.2)
        self.assertEqual(result, "LONG_BLINK")

    def test_threshold_value(self):
        self.assertEqual(config.LONG_BLINK_THRESHOLD, 0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)

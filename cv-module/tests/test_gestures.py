import sys
import os
import time

# Make imports work when running from different directories
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.gestures import BlinkGesture


def test_normal_short_blink():
    """Test basic short blink detection."""
    blink = BlinkGesture()
    
    # Start blink
    gesture = blink.update(is_blink=True)
    assert gesture is None, f"Expected None, got {gesture}"
    
    # End blink (short duration)
    time.sleep(0.1)
    gesture = blink.update(is_blink=False)
    
    assert gesture == "BLINK", f"Expected BLINK, got {gesture}"
    assert blink.count == 1, f"Expected count 1, got {blink.count}"
    print("✓ Normal short blink test passed")


def test_long_blink():
    """Test long blink detection."""
    blink = BlinkGesture()
    
    gesture = blink.update(is_blink=True)
    assert gesture is None
    
    time.sleep(0.6)  # longer than LONG_BLINK_THRESHOLD
    gesture = blink.update(is_blink=False)
    
    assert gesture == "LONG_BLINK"
    assert blink.count == 1
    print("✓ Long blink test passed")


def test_face_loss_mid_blink():
    """Test the reset() fix."""
    blink = BlinkGesture()
    
    blink.update(is_blink=True)
    time.sleep(0.1)
    blink.reset()
    gesture = blink.update(is_blink=False)
    
    assert gesture is None
    assert blink.count == 0
    print("✓ Face loss mid-blink reset test passed")


if __name__ == "__main__":
    test_normal_short_blink()
    test_long_blink()
    test_face_loss_mid_blink()
    print("\n✅ All gesture tests passed!")

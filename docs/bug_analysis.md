# Project Analysis: Eye-To-Speak

I have performed a deep-dive analysis of your entire `cv-module` and `core` architecture. Overall, the modularity is excellent and the logic is sound. However, since this is a medical assistive tool, there are a few edge cases and bugs we must patch before it is considered "production-ready".

## 🐞 Identified Bugs & Edge Cases

### 1. Division by Zero Crash (`eye_tracker.py`)
**Severity: High (App Crash)**
*   **The Issue:** In the `eye_aspect_ratio` function, you calculate the horizontal distance `C` across the eye. If the camera glitches or the user is extremely far away, and those two points map to the exact same pixel, `C` becomes `0.0`. The subsequent division `(A + B) / (2.0 * C)` will throw a `ZeroDivisionError` and crash the entire application instantly.
*   **The Fix:** Change the division to use a tiny safety buffer: `(A + B) / (2.0 * max(C, 1e-6))`.

### 2. Config Validation Flaw (`config.py`)
**Severity: Medium (Logic Break)**
*   **The Issue:** The `validate_config()` function checks if `LONG_BLINK_THRESHOLD` is greater than `BLINK_COOLDOWN`. However, it does NOT check the new `EMERGENCY_CLOSURE_THRESHOLD`. If someone accidentally configures `EMERGENCY_CLOSURE_THRESHOLD = 0.4` (which is less than the long blink threshold), the system will trigger an emergency every time they try to do a long blink.
*   **The Fix:** Add a check: `if EMERGENCY_CLOSURE_THRESHOLD <= LONG_BLINK_THRESHOLD: raise ValueError(...)`.

### 3. Emergency Cooldown Bypass (`gestures.py`)
**Severity: Low (Spurious Input)**
*   **The Issue:** When an emergency closure triggers, `self.last_blink` is intentionally bypassed. However, when the user finally opens their eyes again, `self.last_blink` is never updated. This means the very next blink they perform might not respect the `BLINK_COOLDOWN` window, potentially causing a double-count.
*   **The Fix:** Update `self.last_blink = now` when resetting from an emergency trigger.

---

## 🎨 User Experience (UX) Improvements

### 1. Visualizing the Buffer
Currently, the OpenCV window tells you if the eye is "BLINK" or "OPEN". But if you perform a `Long Blink`, the user has to wait 1.5 seconds in silence wondering if the camera caught it before it speaks.
*   **Recommendation:** Draw the `pattern_buffer` on the screen in real-time. If they do a long blink, the screen should immediately display `[ L ]` so they know it registered, and they can confidently do a short blink to make it `[ L, S ]` before the timeout.

### 2. Persistent Calibration
Every time the app restarts, the user has to hold perfectly still for 100 frames to calibrate.
*   **Recommendation:** Save the `current_threshold` to a `settings.json` file. On startup, load the previous threshold so the user can start talking immediately without re-calibrating.

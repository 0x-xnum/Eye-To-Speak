EAR_THRESHOLD = 0.20

BLINK_COOLDOWN = 0.3

CALIBRATION_FRAMES = 100
CALIBRATION_FACTOR = 0.75

LONG_BLINK_THRESHOLD = 0.5

EMERGENCY_CLOSURE_THRESHOLD = 3.0

PATTERN_DICTIONARY = {
    # Conversational
    "S": "Yes",
    "SS": "No",
    "SSS": "I don't know, or Maybe",
    "SL": "Thank you",
    "SLS": "Please repeat that",
    
    # Needs
    "L": "I need help",
    "LS": "I am thirsty or hungry",
    "LL": "I am uncomfortable, please move me",
    
    # System
    "LSS": "Open Keyboard Mode"
}

def validate_config():
    """
    Sanity-checks config values. Raises ValueError with a clear
    message if something is set to a value that would produce
    confusing or broken behavior at runtime.
    """

    if EAR_THRESHOLD <= 0:
        raise ValueError(
            "EAR_THRESHOLD must be > 0"
        )

    if not (0 < CALIBRATION_FACTOR < 1):
        raise ValueError(
            "CALIBRATION_FACTOR must be between 0 and 1"
        )

    if CALIBRATION_FRAMES <= 0:
        raise ValueError(
            "CALIBRATION_FRAMES must be > 0"
        )

    if BLINK_COOLDOWN < 0:
        raise ValueError(
            "BLINK_COOLDOWN cannot be negative"
        )

    if LONG_BLINK_THRESHOLD <= BLINK_COOLDOWN:
        raise ValueError(
            "LONG_BLINK_THRESHOLD must be greater than "
            "BLINK_COOLDOWN, otherwise long blinks become "
            "indistinguishable from the debounce window"
        )
        
    if EMERGENCY_CLOSURE_THRESHOLD <= LONG_BLINK_THRESHOLD:
        raise ValueError(
            "EMERGENCY_CLOSURE_THRESHOLD must be greater than "
            "LONG_BLINK_THRESHOLD"
        )

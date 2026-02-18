import os

COLOR_ENABLED = os.environ.get("TVX_COLOR", "1") == "1"

def c(text, code):
    if not COLOR_ENABLED:
        return text
    return f"\033[{code}m{text}\033[0m"

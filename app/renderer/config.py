from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "app"
CACHE_DIR = ROOT / "cache"
OUTPUT_DIR = ROOT / "output"
ASSETS_DIR = ROOT / "assets"
TEMP_DIR = CACHE_DIR / "_tmp"

SUPPORTED_CAMERA = {
    "STATIC", "ZOOM_IN_SLOW", "ZOOM_OUT_SLOW",
    "PAN_LEFT", "PAN_RIGHT", "PAN_UP", "PAN_DOWN",
    "PUNCH_ZOOM", "SHAKE_LIGHT",
}
SUPPORTED_TRANSITIONS = {"CUT", "CROSSFADE", "FADE_IN", "FADE_OUT", "FLASH"}
SUPPORTED_TEXT_TYPES = {"situation_label", "dialogue", "thought", "caption", "ui", "end_message"}
SUPPORTED_ACTION_TYPES = {"IMAGE_SWAP", "IMAGE_SEQUENCE", "CURSOR_MOVE", "CURSOR_CLICK"}
SUPPORTED_ACTION_TRANSITIONS = {"CUT", "CROSSFADE"}
DEFAULT_TRANSITION_DURATION = 0.22
DEFAULT_FONT_SIZE = {
    "situation_label": 44,
    "dialogue": 58,
    "thought": 56,
    "caption": 50,
    "ui": 44,
    "end_message": 52,
}

# Audio V1 official logical key for ordinary cursor/UI click feedback.
OFFICIAL_UI_CLICK_SFX = "light-click"

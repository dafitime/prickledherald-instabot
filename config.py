# config.py
import config
from importlib import reload
reload(config)  # Force reload to avoid stale imports

# Static paths
LOGO_PATH = "assets/logo.png"
FONT_PATH = "assets/Nexa-XBold.ttf"

# Dimensions
FINAL_WIDTH = 1080  # Full width of the final image
FINAL_HEIGHT = 1080  # Full height of the final image
IMAGE_HEIGHT = 680  # Hardcoded final image height
TEXTBOX_HEIGHT = 250  # Finalized text box height
LOGOBOX_HEIGHT = FINAL_HEIGHT - IMAGE_HEIGHT - TEXTBOX_HEIGHT  # Automatically calculated
LOGO_SIZE = int(140)  # Ensure it's an integer
DEFAULT_LOGO_SIZE = int(140)  # Default size of logo

# Default values
DEFAULT_FONT_SIZE = 55  # Slightly reduced font size to prevent text overflow
DEFAULT_ZOOM = 120  # Default image zoom percentage
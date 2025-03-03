from PIL import Image
import config


def process_image(image_path, zoom_level, target_width=1080, target_height=680):
    """
    Processes the image: zooms into the center, crops or pads to ensure
    the final image is exactly 1080x680 with the content centered.
    """
    # Load image and convert to RGBA to handle transparency
    image = Image.open(image_path).convert("RGBA")
    
    # Get original dimensions
    orig_width, orig_height = image.size
    
    # Calculate zoom factor
    zoom_factor = zoom_level / 100
    
    # Determine new dimensions after zooming
    new_width = int(orig_width * zoom_factor)
    new_height = int(orig_height * zoom_factor)
    
    # Resize the image
    image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Calculate centered crop coordinates
    center_x = new_width // 2
    center_y = new_height // 2
    left = max(0, center_x - (target_width // 2))
    right = min(new_width, center_x + (target_width // 2))
    top = max(0, center_y - (target_height // 2))
    bottom = min(new_height, center_y + (target_height // 2))
    
    # Perform the crop
    image = image.crop((left, top, right, bottom))
    
    # Create a target-sized canvas with transparency
    if image.size != (target_width, target_height):
        canvas = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        # Calculate position to center the cropped image
        paste_x = (target_width - image.width) // 2
        paste_y = (target_height - image.height) // 2
        canvas.paste(image, (paste_x, paste_y))
        image = canvas
    
    return image




def add_logo(canvas):
    """Adds the logo to the canvas."""
    logo = Image.open(config.LOGO_PATH).convert("RGBA")
    logo = logo.resize((config.LOGOBOX_HEIGHT, config.LOGOBOX_HEIGHT), Image.Resampling.LANCZOS)

    logo_x = (config.FINAL_WIDTH - config.LOGOBOX_HEIGHT) // 2
    logo_y = config.FINAL_HEIGHT - config.LOGOBOX_HEIGHT - 10

    canvas.paste(logo, (logo_x, logo_y), logo)
    return canvas

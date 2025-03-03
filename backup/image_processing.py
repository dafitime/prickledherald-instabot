from PIL import Image, ImageDraw, ImageFont
import config
import textwrap


def process_image(featured_image_path, zoom_percent):
    """Processes the featured image by scaling and cropping it."""
    featured_image = Image.open(featured_image_path)

    zoom_factor = zoom_percent / 100.0
    scaled_width = int(featured_image.width * zoom_factor)
    scaled_height = int(featured_image.height * zoom_factor)

    scaled_image = featured_image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

    left = max(0, (scaled_width - config.FINAL_WIDTH) // 2)
    right = left + config.FINAL_WIDTH
    top = max(0, (scaled_height - config.IMAGE_HEIGHT) // 2)
    bottom = top + config.IMAGE_HEIGHT

    cropped_image = scaled_image.crop((left, top, right, bottom))

    return cropped_image


def add_logo(canvas):
    """Adds the logo to the canvas."""
    logo = Image.open(config.LOGO_PATH).convert("RGBA")
    logo = logo.resize((config.LOGOBOX_HEIGHT, config.LOGOBOX_HEIGHT), Image.Resampling.LANCZOS)

    logo_x = (config.FINAL_WIDTH - config.LOGOBOX_HEIGHT) // 2
    logo_y = config.FINAL_HEIGHT - config.LOGOBOX_HEIGHT - 10

    canvas.paste(logo, (logo_x, logo_y), logo)
    return canvas

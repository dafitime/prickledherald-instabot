from PIL import ImageDraw, ImageFont
import config
import textwrap


def wrap_text(title_text, font_size):
    """Wraps text to fit inside the text box area."""
    text_font = ImageFont.truetype(config.FONT_PATH, font_size)
    wrapped_text = textwrap.fill(title_text, width=35)
    return wrapped_text.split("\n"), text_font


def draw_text(canvas, text_lines, text_font):
    """Draws wrapped text onto the canvas."""
    draw = ImageDraw.Draw(canvas)

    line_height = draw.textbbox((0, 0), "A", font=text_font)[3]
    total_text_height = len(text_lines) * line_height + (len(text_lines) - 1) * 10
    text_y = config.IMAGE_HEIGHT + ((config.TEXTBOX_HEIGHT - total_text_height) // 2)

    for line in text_lines:
        text_x = (config.FINAL_WIDTH - draw.textbbox((0, 0), line, font=text_font)[2]) // 2
        draw.text((text_x, text_y), line, font=text_font, fill="black")
        text_y += line_height + 10

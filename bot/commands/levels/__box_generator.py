from PIL import Image, ImageDraw
from io import BytesIO
import discord
def generate_color_square(color: tuple[int, int, int]) -> Image:
    """
    Generate a color square based on the color provided.

    Parameters
    ----------
    color : tuple[int, int, int]
        The color to be used.

    Returns
    -------
    Image
        The color square.
    """
    color_square = Image.new("RGB", (100, 100))
    draw = ImageDraw.Draw(color_square)
    draw.rectangle((0, 0, 100, 100), fill=color)
    bytes = BytesIO()
    color_square.save(bytes, "png")
    bytes.seek(0)
    return discord.File(bytes, filename="color_square.png")
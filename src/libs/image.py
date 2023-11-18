from pathlib import Path
from PIL import Image, ImageEnhance

from config import PAGE_HEIGHT


def edit_image(open_image_pillow: Image, path_save: Path) -> None:
    # image edit

    enhancer = ImageEnhance.Contrast(open_image_pillow)
    image_output = enhancer.enhance(2)

    enhancer = ImageEnhance.Brightness(open_image_pillow)
    image_output = enhancer.enhance(1.2)

    image_output.save(path_save)


def resize_image(img: Path) -> tuple:
    image_pil = Image.open(img)
    real_width, real_height = image_pil.size

    ratio = PAGE_HEIGHT / real_height
    width = int(real_width*ratio)

    image_pil.resize((width, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    image_pil.save(img)

    # edit_image(image_pil, img)

    return width, PAGE_HEIGHT

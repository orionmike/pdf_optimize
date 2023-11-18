from pathlib import Path
from PIL import Image, ImageEnhance

from config import IMG_BLACK_WHITE, IMG_BRIGHTNESS, IMG_CONTRAST, IS_EDIT_IMG, PAGE_HEIGHT


def edit_image(open_image_pillow: Image, path_save: Path) -> None:
    # image edit

    if IMG_BLACK_WHITE:
        open_image_pillow = open_image_pillow.convert("L")

    if IMG_CONTRAST != 1:
        enhancer = ImageEnhance.Contrast(open_image_pillow)
        image_output = enhancer.enhance(IMG_CONTRAST)

    if IMG_BRIGHTNESS != 1:
        enhancer = ImageEnhance.Brightness(open_image_pillow)
        image_output = enhancer.enhance(IMG_BRIGHTNESS)

    image_output.save(path_save)


def resize_image(img: Path) -> tuple:
    image_pil = Image.open(img)
    real_width, real_height = image_pil.size

    ratio = PAGE_HEIGHT / real_height
    width = int(real_width*ratio)

    image_pil.resize((width, PAGE_HEIGHT), Image.Resampling.LANCZOS)

    if IS_EDIT_IMG:
        edit_image(image_pil, img)
    else:
        image_pil.save(img)

    return width, PAGE_HEIGHT

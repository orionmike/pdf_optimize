import shutil
from datetime import datetime
from pathlib import Path

import fitz
from colorama import Fore
from tqdm import tqdm

from config import (IND, JPG_QUALITY, MIN_SIZE_FILE, PATH_FILES_TEMP,
                    PATH_IMG_TEMP, PDF_DPI, logger)
from libs.file import (
    create_fodler_path, delete_file_list,
    get_correct_file_size, get_correct_size,
    get_path_file_output)
from libs.image import resize_image
from libs.utils import get_dt_now, get_percent_optimize, print_time_operation


def get_image_list_from_pdf(file) -> int:

    pdf_document = fitz.open(file)

    image_list = []

    for page in tqdm(pdf_document, desc=f'{IND*2} unpack pdf'):  # iterate through the pages
        pix = page.get_pixmap(dpi=PDF_DPI)  # render page to an image
        page_file_name = f'{PATH_IMG_TEMP}/{page.number:04}.jpg'
        pix.pil_save(page_file_name, quality=JPG_QUALITY)

        image_list.append(Path(page_file_name))

    # image_list_2 = list(PATH_IMG_TEMP.glob('**/*.jpg'))
    # print(len(image_list), len(image_list_2))

    return image_list


def make_pdf_from_image_list(pdf_file_name, img_list: list) -> int:

    try:
        pdf_doc = fitz.open()

        for page_number, img in enumerate(tqdm(img_list, desc=f'{IND*2} build pdf')):

            width, height = resize_image(img)
            pdf_doc.new_page(width=width, height=height)
            rect = fitz.Rect(0, 0, width, height)

            pdf_doc[page_number].insert_image(rect, filename=img)

        pdf_doc.save(f'{PATH_FILES_TEMP}/{pdf_file_name}')
        file = Path(f'{PATH_FILES_TEMP}/{pdf_file_name}')

        file_size = get_correct_file_size(file)

        print(f"{IND*2} output file size: {Fore.YELLOW}{file_size.correct_size} {file_size.unit}")

        delete_file_list(img_list)

        return file_size.file_size

    except Exception as e:
        print(f"{Fore.RED}{IND*2} make_pdf_from_image_list -> {e}")


def get_output_file(file: Path, file_input_size: int, file_output_size: int) -> None:

    path_result_file = get_path_file_output(file)
    create_fodler_path(path_result_file.parent)

    if file_output_size < file_input_size:

        freed_memory = get_correct_size(file_input_size - file_output_size)

        try:

            if not path_result_file.exists():
                shutil.move(f'{PATH_FILES_TEMP}/{file.name}', path_result_file)
            else:
                path_result_file.unlink()
                shutil.move(f'{PATH_FILES_TEMP}/{file.name}', path_result_file)

            percent_optimize = get_percent_optimize(file_input_size, file_output_size)

            file.unlink()

            print(f'{IND*2} {Fore.YELLOW}optimization: {Fore.GREEN}OK -> {percent_optimize}%')
            logger.info(f'{file}\n{IND}{path_result_file}\n')

        except Exception as e:
            print(f'{IND*2} {Fore.RED}f:check_and_save_file: optimization: Error -> {e}')

        print(f'{IND*2} {Fore.YELLOW}freed memory: {Fore.GREEN}{freed_memory.correct_size} {freed_memory.unit}')
    else:
        print(f'{IND*2} {Fore.YELLOW}optimization: {Fore.RED}NOT')
        Path(f'{PATH_FILES_TEMP}/{file.name}').unlink()

        shutil.move(file, path_result_file)


def optimize_file_list_recursive(path: Path) -> None:

    if path.exists():

        for path_object in path.iterdir():

            if path_object.is_dir():
                optimize_file_list_recursive(path_object)
                path_object.rmdir()

            else:

                if path_object.suffix == '.pdf':
                    file = path_object

                    if file.stat().st_size > 1024 * MIN_SIZE_FILE:

                        start = datetime.now()

                        print(f'{get_dt_now()} -> {path_object}')

                        file_input_size = get_correct_file_size(file)

                        print(f"{IND} input file: {Fore.CYAN}{file.name}")
                        print(f"{IND*2} file size: {Fore.YELLOW}{file_input_size.correct_size} {file_input_size.unit}")

                        img_list = get_image_list_from_pdf(file)
                        print(f"{IND*2} pages: {Fore.YELLOW}{len(img_list)}")

                        file_output_size = make_pdf_from_image_list(file.name, img_list)

                        get_output_file(file, file_input_size.file_size, file_output_size)

                        print_time_operation(start, message=f'{IND} time of processing:')
                        print()
                    else:
                        path_result_file = get_path_file_output(file)
                        create_fodler_path(path_result_file.parent)
                        shutil.move(file, path_result_file)

                else:
                    path_result_file = get_path_file_output(path_object)
                    create_fodler_path(path_result_file.parent)
                    print(f'{IND} file [{path_object}] is not a pdf')
                    shutil.move(path_object, path_result_file)

    else:
        print(f'path [{path.resolve()}] not exist')

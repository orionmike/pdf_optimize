import sys
from datetime import datetime
from pathlib import Path

from colorama import Fore, Style, init
from loguru import logger

init(autoreset=True)


ABS_PATH = Path('./src').resolve()  # windows
# ABS_PATH = sys.path[0]  # linux
APP_NAME = 'pdf_optimize'

try:

    if sys.version_info.major == 3 and sys.version_info.minor >= 11:

        import tomllib
        with open(f"{ABS_PATH}/config.toml", "rb") as f:
            config = tomllib.load(f)
    else:

        import toml  # pip install toml
        with open(f"{ABS_PATH}/config.toml", "r") as f:
            config = toml.load(f)

    IND = config['utils']['console_indent']

    # settings path
    PATH_FILES_INPUT = Path(config['path']['dir_files_input'])
    PATH_FILES_TEMP = config['path']['dir_files_temp']
    PATH_FILES_OUTPUT = config['path']['dir_files_output']
    PATH_IMG_TEMP = Path(config['path']['dir_img_temp'])

    # settings optimization
    PDF_DPI = int(config['optimize']['dpi'])
    JPG_QUALITY = int(config['optimize']['jpg_quality'])
    MIN_SIZE_FILE = int(config['optimize']['min_size_file'])
    PAGE_HEIGHT = int(config['optimize']['page_heigth'])

    # settings service
    TIME_SCAN_INPUT_DIR = int(config['service']['time_scan_input_dir'])

    # logging
    log_file_name = f'{datetime.now().strftime("%Y-%m-%d")}'
    logger.remove()
    logger.add(f'{ABS_PATH}/logs/{log_file_name}.log', format='{time} {level} {message}', level='INFO', rotation='1 day')

    print(f'{APP_NAME}')
    print(f'{IND} python {sys.version_info.major}.{sys.version_info.minor}')
    print()

    print(f'{IND} path input files: {Fore.YELLOW}{PATH_FILES_INPUT}')
    print(f'{IND} path output files: {Fore.YELLOW}{PATH_FILES_OUTPUT}')
    print(f'{IND} dpi: {Fore.YELLOW}{PDF_DPI}')
    print(f'{IND} jpg quality: {Fore.YELLOW}{JPG_QUALITY}')
    print(f'{IND} min file size: {Fore.YELLOW}{MIN_SIZE_FILE} kb')
    print()

except Exception as e:
    raise Exception(f'config load -> error: {e}')


import time
from datetime import datetime
from pathlib import Path

import schedule
from colorama import Fore

from config import IND, PATH_FILES_INPUT, TIME_SCAN_INPUT_DIR
from libs.file import get_count_files_recursive
from libs.pdf import optimize_file_list_recursive


def pdf_optimize() -> None:

    try:
        path_files = Path(PATH_FILES_INPUT)
        count_file_start = get_count_files_recursive(path_files)

        if count_file_start > 0:

            print(f'{Fore.YELLOW}{datetime.now()} detect files: {Fore.CYAN}{count_file_start}')

            time.sleep(10)
            count_file_check = get_count_files_recursive(path_files)

            if count_file_start == count_file_check:
                optimize_file_list_recursive(path_files)
            else:
                print(f'{datetime.now()} check list files: {Fore.RED}false')

    except Exception as e:
        print(f'{Fore.RED}{e}')
        # input('Press any key tocontinue')


if __name__ == "__main__":

    print(f'{IND} time period scan: {Fore.YELLOW}{TIME_SCAN_INPUT_DIR} min')

    schedule.every(TIME_SCAN_INPUT_DIR).minutes.do(pdf_optimize)

    while True:
        schedule.run_pending()
        time.sleep(1)

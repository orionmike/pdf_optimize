
from datetime import datetime

from colorama import Fore


def get_dt_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def print_time_operation(start_time, message=' > time operation:'):
    result_dt = datetime.now().timestamp() - start_time.timestamp()
    result = datetime.fromtimestamp(int(result_dt)).strftime('%M:%S')

    print(f'{message} {Fore.CYAN}{result}')


def get_percent_optimize(file_size_input, file_size_output) -> float:
    return round(100 - (file_size_output / file_size_input * 100), 2)


def get_file_size_mb(size_byte: int) -> float:
    return round(size_byte / (1024 * 1024), 2)

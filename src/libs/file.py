import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

from config import PATH_FILES_INPUT, PATH_FILES_OUTPUT


@dataclass
class FileSize:
    file_size: int
    correct_size: int
    unit: str = 'kb'


def get_correct_file_size(file: Path) -> FileSize:

    file_size_bite = file.stat().st_size
    result = FileSize(file_size_bite, round(file_size_bite / 1024, 2))

    if file_size_bite > 1024 * 1024:
        result = FileSize(file_size_bite, round(file_size_bite / (1024 * 1024), 2), 'mb')

    return result


def get_correct_size(count_bytes: int) -> FileSize:

    result = FileSize(count_bytes, round(count_bytes / 1024, 2))

    if count_bytes > 1024 * 1024:
        result = FileSize(count_bytes, round(count_bytes / (1024 * 1024), 2), 'mb')

    return result


def create_fodler_path(path: Path) -> None:
    if not path.exists():
        path_result = Path(path.parts[0])
        # print(path.parts)
        for index_dir, _ in enumerate(path.parts):
            if index_dir > 0:
                path_result = path_result.joinpath(path.parts[index_dir])
                if not path_result.exists():
                    path_result.mkdir()


def get_path_file_output(path_object: Path) -> Path:
    path_in = str(Path(PATH_FILES_INPUT)).replace('\\', '/')
    path_out = str(Path(PATH_FILES_OUTPUT)).replace('\\', '/')
    path = str(path_object).replace('\\', '/')

    return Path(re.sub(rf'^{path_in}', path_out, path))


def get_count_files_recursive(path: Path, count_file: int = 0) -> int:

    count_final = count_file

    for path_object in path.iterdir():

        if path_object.is_dir():
            count_final = get_count_files_recursive(path_object,  count_file=count_final)
        else:
            count_final += 1
            # print(f'{count_f} {path_object}')

    return count_final


def delete_file_list(file_list: List[Path]) -> None:
    for file in file_list:
        file.unlink()

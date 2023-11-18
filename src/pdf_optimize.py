
from config import PATH_FILES_INPUT
from libs.pdf import optimize_file_list_recursive

if __name__ == "__main__":
    optimize_file_list_recursive(PATH_FILES_INPUT)
    input('Press any key to continue')

from os.path import isdir, isfile
from pathlib import Path


def get_initial_write_data(file_path):
    path = Path(file_path)
    if isdir(file_path):
        directory_scan(path)
    elif isfile(file_path):
        return 1, path.stat().st_size


def directory_scan(path, current_file_count=0, current_byte_count=0):
    return current_file_count, current_byte_count


def file_scan(path):
    return path.stat().st_size


d = get_initial_write_data('/home/m/Desktop/hadouken.gif')
print(d)
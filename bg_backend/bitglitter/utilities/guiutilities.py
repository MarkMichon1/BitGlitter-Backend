from os.path import isdir, isfile
from pathlib import Path


def directory_scan(path, current_file_count=0, current_byte_count=0):
    """Recursively traverses directories, returning number of files as well as total size in bytes."""
    current_file_count = current_file_count
    current_byte_count = current_byte_count

    files = []
    subdirectories = []
    sorted_glob = sorted(path.glob('*'))
    for item in sorted_glob:
        if item.is_file():
            files.append(item)
        else:
            subdirectories.append(item)

    if files:
        for file in files:
            current_byte_count += file_scan(file)
            current_file_count += 1

    if subdirectories:
        for subdirectory in subdirectories:
            current_file_count, current_byte_count = directory_scan(subdirectory, current_file_count,
                                                                    current_byte_count)

    return current_file_count, current_byte_count


def file_scan(path):
    """Returns the size in bytes from a given file path."""
    return path.stat().st_size


def get_initial_write_data(file_path):
    """Returns number of files, and sum of their file size in bytes."""
    path = Path(file_path)
    if isdir(path):
        return directory_scan(path)
    elif isfile(path):
        return 1, file_scan(path)

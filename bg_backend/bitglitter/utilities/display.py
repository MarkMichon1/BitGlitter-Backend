def humanize_file_size(size_in_bytes):
    if not size_in_bytes:
        return 'None'
    elif 0 < size_in_bytes < 1000:
        return f'{size_in_bytes} B'
    elif 1000 <= size_in_bytes < 1000 ** 2:
        return f'{round((size_in_bytes / 1000), 2)} KB'
    elif 1000 ** 2 <= size_in_bytes < 1000 ** 3:
        return f'{round((size_in_bytes / 1000 ** 2), 2)} MB'
    elif 1000 ** 3 <= size_in_bytes < 1000 ** 4:
        return f'{round((size_in_bytes / 1000 ** 3), 2)} GB'
    elif 1000 ** 4 <= size_in_bytes < 1000 ** 5:
        return f'{round((size_in_bytes / 1000 ** 4), 2)} TB'
    elif 1000 ** 5 <= size_in_bytes < 1000 ** 6:
        return f'{round((size_in_bytes / 1000 ** 5), 2)} PB'


def humanize_integer_comma(integer):
    return "{:,}".format(integer) if integer else 0
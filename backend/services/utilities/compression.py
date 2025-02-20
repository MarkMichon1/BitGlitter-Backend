import os
import brotli


DEFAULT_QUALITY = 11 #todo address levels
BROTLI_STRENGTH_DICT = {1 : 1,
        2 : 4,
        3 : 7,
        4 : 10,
        5 : 11,}


def compress_file(input_file, output_file, write_mode, remove_input=True):
    """This inputs a file, and writes a compressed one, removing the input file afterwards by default."""
    if write_mode == 'write':
        mode = 'wb'
    elif write_mode == 'append':
        mode = 'ab'
    else:
        raise ValueError("'write' and 'append' are the only allowed strings for write_mode.")

    total_size = os.path.getsize(input_file)
    bytes_read = 0

    # Use the current DEFAULT_QUALITY
    compressor = brotli.Compressor(quality=DEFAULT_QUALITY)
    with open(input_file, 'rb') as decompressed:
        with open(output_file, mode) as compressed:
            chunk_size = 1000000
            while True:
                chunk = decompressed.read(chunk_size)
                if chunk:
                    bytes_read += len(chunk)
                    progress = (bytes_read / total_size) * 100
                    # print(f"Progress: {progress:.2f}%")
                    compressed.write(compressor.process(chunk))
                else:
                    compressed.write(compressor.finish())
                    break

    if remove_input:
        os.remove(input_file)


def compress_bytes(input_bytes):
    compressed = brotli.compress(input_bytes, quality=DEFAULT_QUALITY)
    return compressed


def decompress_file(input_file, output_file, remove_input=True):
    """Doing the opposite as compress_file(), this inputs a compressed file, and writes a decompressed one, while
    removing the original file by default.
    """
    total_size = os.path.getsize(input_file)
    bytes_read = 0

    decompressor = brotli.Decompressor()
    with open(input_file, 'rb') as compressed:
        with open(output_file, 'wb') as decompressed:
            chunk_size = 1000000
            while True:
                chunk = compressed.read(chunk_size)
                if chunk:
                    bytes_read += len(chunk)
                    progress = (bytes_read / total_size) * 100
                    # print(f"Progress: {progress:.2f}%")
                    decompressed.write(decompressor.process(chunk))
                else:
                    break

    if remove_input:
        os.remove(input_file)


def decompress_bytes(input_bytes):
    decompressed = brotli.decompress(input_bytes)
    return decompressed

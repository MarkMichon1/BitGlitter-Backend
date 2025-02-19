import multiprocessing
import os

import brotli

CHUNK_SIZE = 1024 ^ 2

def compress_file(input_file, output_file, write_mode, remove_input=True):
    """Compresses a file in chunks to prevent excessive memory usage."""
    if write_mode == 'write':
        mode = 'wb'
    elif write_mode == 'append':
        mode = 'ab'
    else:
        raise ValueError("'write' and 'append' are the only allowed strings for write_mode.")

    compressor = brotli.Compressor(quality=11)
    with open(input_file, 'rb') as decompressed, open(output_file, mode) as compressed:
        while chunk := decompressed.read(CHUNK_SIZE):
            compressed.write(compressor.process(chunk))  # ✅ Correct API usage
        compressed.write(compressor.finish())  # Ensures all remaining compressed data is written

    if remove_input:
        os.remove(input_file)


def compress_bytes(input_bytes):
    return brotli.compress(input_bytes, quality=11)


def decompress_file(input_file, output_file, remove_input=True):
    """Decompresses a file in chunks to prevent excessive memory usage."""
    decompressor = brotli.Decompressor()
    with open(input_file, 'rb') as compressed, open(output_file, 'wb') as decompressed:
        while chunk := compressed.read(CHUNK_SIZE):
            decompressed.write(decompressor.process(chunk))  # ✅ Correct API usage
        decompressed.write(decompressor.finish())  # Ensures all remaining decompressed data is written

    if remove_input:
        os.remove(input_file)


def decompress_bytes(input_bytes):
    return brotli.decompress(input_bytes)


# Testing compression and decompression of a test file
test_file_path = "/home/m/Desktop/1.pdf"
compressed_test_file_path = "/home/m/Desktop/test.txt.br"
decompressed_test_file_path = "/home/m/Desktop/test_decompressed.txt"

# Uncomment one at a time to test
compress_file(test_file_path, compressed_test_file_path, "write", remove_input=False)
# decompress_file(compressed_test_file_path, decompressed_test_file_path, remove_input=False)

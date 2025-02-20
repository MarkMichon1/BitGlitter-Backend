from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

import hashlib
from io import BytesIO
import os
import secrets
import string


ARGON2ID_STRENGTH_DICT = {
    1: {'memory_cost': 19000, 'iterations': 2, 'parallelism': 1},
    2: {'memory_cost': 30000, 'iterations': 3, 'parallelism': 1},
    3: {'memory_cost': 42000, 'iterations': 4, 'parallelism': 2},
    4: {'memory_cost': 55000, 'iterations': 5, 'parallelism': 2},
    5: {'memory_cost': 70000, 'iterations': 6, 'parallelism': 2},
}


def _derive_key(password, salt, crypto_strength):
    key = hash_secret_raw(
        password.encode(),
        salt,
        time_cost=ARGON2ID_STRENGTH_DICT[crypto_strength]['iterations'],
        memory_cost=ARGON2ID_STRENGTH_DICT[crypto_strength]['memory_cost'],
        parallelism=ARGON2ID_STRENGTH_DICT[crypto_strength]['parallelism'],
        hash_len=32,
        type=Type.ID
    )
    return key


def encrypt_file(input_file, output_file, write_mode, encryption_key, argon2id_strength, remove_input=True):
    """
    Encrypts input_file using AES-CBC with PKCS7 padding. The IV and salt are prepended to the encrypted output.
    """
    if write_mode == 'write':
        mode = 'wb'
    elif write_mode == 'append':
        mode = 'ab'
    else:
        raise ValueError('Only "write" and "append" are allowed for write_mode.')

    backend = default_backend()
    initialization_vector = os.urandom(AES.block_size // 8)
    salt = os.urandom(AES.block_size // 8)
    key = _derive_key(encryption_key, salt, argon2id_strength)

    cipher = Cipher(AES(key), modes.CBC(initialization_vector), backend=backend)
    encryptor = cipher.encryptor()
    padder = PKCS7(AES.block_size).padder()

    with open(output_file, mode) as file_out:
        # Write IV and salt first
        file_out.write(initialization_vector)
        file_out.write(salt)
        with open(input_file, 'rb') as file_in:
            while True:
                chunk = file_in.read(1048576)  # 1 MB chunks
                if not chunk:
                    break
                # Update the padder with new data
                padded_data = padder.update(chunk)
                if padded_data:
                    file_out.write(encryptor.update(padded_data))
            # Finalize padding and encryption
            padded_data = padder.finalize()
            file_out.write(encryptor.update(padded_data) + encryptor.finalize())

    if remove_input:
        os.remove(input_file)


def decrypt_file(input_file, output_file, encryption_key, argon2id_strength, remove_input=True):
    """
    Decrypts a file that was encrypted with encrypt_file(). Expects the IV and salt to be at the beginning of the file.
    """
    backend = default_backend()
    with open(input_file, 'rb') as file_in:
        initialization_vector = file_in.read(AES.block_size // 8)
        salt = file_in.read(AES.block_size // 8)
        key = _derive_key(encryption_key, salt, argon2id_strength)
        cipher = Cipher(AES(key), modes.CBC(initialization_vector), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = PKCS7(AES.block_size).unpadder()

        with open(output_file, 'wb') as file_out:
            while True:
                chunk = file_in.read(1048576)
                if not chunk:
                    break
                decrypted_data = decryptor.update(chunk)
                if decrypted_data:
                    file_out.write(unpadder.update(decrypted_data))
            # Finalize decryption and unpadding
            decrypted_data = decryptor.finalize()
            file_out.write(unpadder.update(decrypted_data) + unpadder.finalize())

    if remove_input:
        os.remove(input_file)


def encrypt_bytes(input_bytes, encryption_key, argon2id_strength):
    """
    Encrypts bytes data with AES-CBC and PKCS7 padding.  Returns initialization vector + salt + encrypted data.
    """

    backend = default_backend()
    initialization_vector = os.urandom(AES.block_size // 8)
    salt = os.urandom(AES.block_size // 8)
    key = _derive_key(encryption_key, salt, argon2id_strength)

    cipher = Cipher(AES(key), modes.CBC(initialization_vector), backend=backend)
    encryptor = cipher.encryptor()
    padder = PKCS7(AES.block_size).padder()

    padded_data = padder.update(input_bytes) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return initialization_vector + salt + encrypted_data


def decrypt_bytes(input_bytes, encryption_key, argon2id_strength):
    """
    Decrypts bytes that were encrypted by encrypt_bytes().
    Expects IV + salt to be prepended to the encrypted data.
    """
    backend = default_backend()
    with BytesIO(input_bytes) as fin:
        initialization_vector = fin.read(AES.block_size // 8)
        salt = fin.read(AES.block_size // 8)
        key = _derive_key(encryption_key, salt, argon2id_strength)
        cipher = Cipher(AES(key), modes.CBC(initialization_vector), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = PKCS7(AES.block_size).unpadder()
        encrypted_data = fin.read()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        try:
            return unpadder.update(decrypted_data) + unpadder.finalize()
        except ValueError:
            return None


def get_sha3_from_file(file_path, byte_output=False):
    """
    Returns the SHA3-256 hash of a file.
    """
    sha3_256 = hashlib.sha3_256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(100000)
            if not data:
                break
            sha3_256.update(data)
    return sha3_256.digest() if byte_output else sha3_256.hexdigest()


def get_sha3_hash_from_bytes(input_bytes, byte_output=False):
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(input_bytes)
    return sha3_256.digest() if byte_output else sha3_256.hexdigest()


def generate_secure_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

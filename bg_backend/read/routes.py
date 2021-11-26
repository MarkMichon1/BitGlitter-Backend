from flask import Blueprint, jsonify, request

import traceback

from bg_backend.bitglitter.config.configfunctions import read_warmup
from bg_backend.bitglitter.config.configmodels import Config
from bg_backend.bitglitter.config.readfunctions import attempt_metadata_decrypt, blacklist_stream_sha256, \
    remove_all_blacklist_sha256, remove_all_partial_save_data, remove_partial_save, return_all_blacklist_sha256, \
    return_all_read_information, return_stream_file_data, return_stream_frame_data, return_stream_progress_data, \
    remove_blacklist_sha256, return_single_read_information, return_stream_manifest, update_decrypt_values, \
    update_stream_read, unpackage, verify_is_bitglitter_file
from bg_backend.bitglitter.read.read import read as read_func
from bg_backend.bitglitter.utilities.gui.messages import read_error_http

read = Blueprint('read', __name__)


@read.route('/read/', methods=['POST'])
def start_read():
    read_values = read_warmup()
    to_dict = request.get_json()
    try:    #todo integrate
        results = read_func(to_dict['something']) #todo- read strikes as int w/o bool toggle
    except:
        print(f'***Exception in read:***\n\n{traceback.format_exc()}')
        read_error_http(traceback.format_exc(), read_values['read_path'])
    return jsonify(results=True)


@read.route('/read/stream-read/unpackage', methods=['POST'])
def unpackage_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    results = unpackage(stream_sha256)
    return jsonify(results=results)


@read.route('/read/stream-read/return-all', methods=['GET'])
def return_all_read_information_route():
    config = Config.query.first()
    display_advanced_data = config.display_advanced_data
    return jsonify(results=return_all_read_information(advanced=display_advanced_data))


# Currently unused; functional if uncommented
# @read.route('/read/stream-read/return-one', methods=['GET'])
# def return_single_read_information_route():
#     to_dict = request.get_json()
#     stream_sha256 = to_dict['stream_sha256']
#     config = Config.query.first()
#     display_advanced_data = config.display_advanced_data
#     return jsonify({'stream': return_single_read_information(stream_sha256, advanced=display_advanced_data)})


@read.route('/read/stream-read/update-crypto', methods=['POST'])
def update_decrypt_values_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    decryption_key = to_dict['decryption_key']
    scrypt_n = to_dict['scrypt_n']
    scrypt_r = to_dict['scrypt_r']
    scrypt_p = to_dict['stream_sha256']
    results = update_decrypt_values(stream_sha256, decryption_key, scrypt_n, scrypt_r, scrypt_p)
    return jsonify(results=results)


@read.route('/read/stream-read/attempt-metadata-decrypt', methods=['POST'])
def attempt_metadata_decrypt_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    results = attempt_metadata_decrypt(stream_sha256)
    return jsonify(results=results)


@read.route('/read/stream-read/return-manifest', methods=['GET'])
def return_stream_manifest_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    results = return_stream_manifest(stream_sha256, return_as_json=True) #todo- let root state determine route access
    return jsonify(results=results)


@read.route('/read/stream-read/remove', methods=['POST'])
def remove_partial_save_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    results = remove_partial_save(stream_sha256)
    return jsonify(results=results)


@read.route('/read/stream-read/remove-all', methods=['POST'])
def remove_all_partial_save_data_route():
    results = remove_all_partial_save_data()
    return jsonify(results=results)


@read.route('/read/stream-read/update', methods=['POST'])
def update_stream_read_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    auto_delete_finished_stream = to_dict['auto_delete_finished_stream']
    auto_unpackage_stream = to_dict['auto_unpackage_stream']
    results = update_stream_read(stream_sha256, auto_delete_finished_stream, auto_unpackage_stream)
    return jsonify(results=results)


@read.route('/read/blacklist/add', methods=['POST'])
def blacklist_stream_sha256_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    results = blacklist_stream_sha256(stream_sha256)
    return jsonify(results=results)


@read.route('/read/blacklist/return-all', methods=['GET'])
def return_all_blacklist_sha256_route():
    return jsonify(blacklist=return_all_blacklist_sha256())


@read.route('/read/blacklist/remove', methods=['POST'])
def remove_blacklist_sha256_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    results = remove_blacklist_sha256(stream_sha256)
    return jsonify(results=results)


@read.route('/read/blacklist/remove-all', methods=['POST'])
def remove_all_blacklist_sha256_route():
    results = remove_all_blacklist_sha256()
    return jsonify(results=results)


@read.route('/read/stream-read/get-frame-data', methods=['GET'])
def return_stream_frame_data_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    results = return_stream_frame_data(stream_sha256)
    return jsonify(results=results)


@read.route('/read/stream-read/get-file-data', methods=['GET'])
def return_stream_file_data_route():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    config = Config.query.first()
    display_advanced_data = config.display_advanced_data
    results = return_stream_file_data(stream_sha256, advanced=display_advanced_data)
    return jsonify(results=results)


@read.route('/read/stream-read/get-progress-data', methods=['GET'])
def return_stream_progress_data():
    to_dict = request.get_json()
    stream_sha256 = to_dict['stream_sha256']
    results = return_stream_progress_data(stream_sha256)
    return jsonify(results=results)


@read.route('/read/stream-verify', methods=['GET'])
def verify_is_bitglitter_file_route():
    to_dict = request.get_json()
    file_path = to_dict['stream_sha256']
    results = verify_is_bitglitter_file(file_path)
    return jsonify(results=results)

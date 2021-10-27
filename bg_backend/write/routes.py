from flask import Blueprint, jsonify, request

import traceback

from bg_backend.bitglitter.config.configfunctions import remove_render_directory, write_warmup
from bg_backend.bitglitter.config.writefunctions import has_one_time_page_ran, one_time_page_has_ran_set
from bg_backend.bitglitter.utilities.gui.files import get_initial_write_data
from bg_backend.bitglitter.utilities.gui.messages import write_error_http
from bg_backend.bitglitter.write.render.renderutilities import total_frames_estimator
from bg_backend.bitglitter.write.write import write as write_func

write = Blueprint('write', __name__)


@write.route('/write/test', methods=['GET'])
def write_socketio_test():
    """Emits a websocket message to check everything is working as it should."""
    socketio.emit('test event', 'test message')
    return jsonify(result=True)


@write.route('/write/show-once', methods=['GET', 'POST'])
def show_once():
    """Returns whether the 'show once' initial screen has been shown already or not.  Sending a POST request sets it
    to True.
    """
    if request.method == 'GET':
        return jsonify(has_ran=has_one_time_page_ran())
    elif request.method == 'POST':
        one_time_page_has_ran_set()
        return jsonify(successful=True)


@write.route('/write/initial-write-data', methods=['POST'])
def initial_write_data():
    """Receives a file path, and returns file count as well as total size in bytes."""
    to_dict = request.get_json()
    results = get_initial_write_data(to_dict['path'])
    return jsonify({'total_files': results[0], 'total_size': results[1]})


@write.route('/write/frame-estimator', methods=['POST'])
def frame_estimator():
    """Receives a file path, and returns file count as well as total size in bytes."""
    to_dict = request.get_json()
    return jsonify({'total_frames': total_frames_estimator(to_dict['block_height'], to_dict['block_width'], 0, 0,
                                                           to_dict['size_in_bytes'] if to_dict['size_in_bytes'] else 0,
                                                           None, to_dict['output_mode'], to_dict['bit_length'])})


@write.route('/write/', methods=['POST'])
def start_write():
    config_values = write_warmup() #path, core count
    to_dict = request.get_json()
    try:
        write_func(input_path=to_dict['input_path'],
                   stream_name=to_dict['stream_name'],
                   stream_description=to_dict['stream_description'],
                   output_directory=config_values['write_path'],
                   output_mode=to_dict['output_mode'],
                   stream_name_file_output=config_values['output_stream_title'],
                   max_cpu_cores=config_values['cpu_cores'],
                   compression_enabled=to_dict['compression_enabled'],
                   file_mask_enabled=to_dict['file_mask_enabled'],
                   encryption_key=to_dict['encryption_key'],
                   scrypt_n=to_dict['scrypt_n'],
                   scrypt_r=to_dict['scrypt_r'],
                   scrypt_p=to_dict['scrypt_p'],
                   stream_palette_id=to_dict['stream_palette_id'],
                   pixel_width=to_dict['pixel_width'],
                   block_height=to_dict['block_height'],
                   block_width=to_dict['block_width'],
                   frames_per_second=to_dict['frames_per_second'],
                   save_statistics=config_values['save_statistics'],
                   bg_version=to_dict['bg_version'],
                   logging_level='debug'
                   )
        return jsonify(result=True)
    except:
        print(f'***Exception in write:***\n\n{traceback.format_exc()}')
        write_error_http(traceback.format_exc(), config_values['write_path'])
        remove_render_directory()
        return jsonify(result=False)

from flask import Blueprint, jsonify, request

from bg_backend import socketio
from bg_backend.bitglitter.config.writefunctions import has_one_time_page_ran, one_time_page_has_ran_set
from bg_backend.bitglitter.utilities.display import humanize_file_size, humanize_integer_comma
from bg_backend.bitglitter.utilities.guiutilities import get_initial_write_data
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
    return jsonify({'total_files': humanize_integer_comma(results[0]), 'total_size': humanize_file_size(results[1])})


@write.route('/write/', methods=['POST'])
def start_write():
    write_func('C:/Users/m/Desktop/test file.mp4')
    return jsonify(result=True)

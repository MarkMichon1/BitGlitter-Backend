from flask import Blueprint, jsonify, request

import traceback

from bg_backend import socketio
from bg_backend.bitglitter.config.configfunctions import read_warmup
from bg_backend.bitglitter.read.read import read as read_func

read = Blueprint('read', __name__)


@read.route('/read/', methods=['POST'])
def start_read():
    read_values = read_warmup()
    to_dict = request.get_json()
    try:
        print('temp placeholder for read reading')
        print(f'{read_values=} {to_dict=}')
        # read_func(to_dict['something']) #todo- read strikes as int w/o bool toggle
    except:
        print(f'***Exception in write:***\n\n{traceback.format_exc()}')
        socketio.emit('read-error', {'error': traceback.format_exc(), 'read_path': read_values['read_path']})
    return jsonify(result=True)


@read.route('/read/get-all', methods=['GET'])
def get_stream_reads():
    return jsonify(streams='123')


@read.route('/read/delete', methods=['GET'])
def delete_stream_reads():
    """Deletes all."""
    return jsonify(streams='123')


@read.route('/read/id/7/update-encryption', methods=['GET'])
def update_encryption_parameters():
    return jsonify(streams='123')


@read.route('/read/id/7/delete', methods=['GET'])
def delete_stream_read():
    return jsonify(streams='123')
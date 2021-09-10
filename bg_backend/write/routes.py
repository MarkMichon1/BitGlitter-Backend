from flask import Blueprint, jsonify, request

from bg_backend import socketio
from bg_backend.bitglitter.write.write import write as write_func


write = Blueprint('write', __name__)


@write.route('/write/test', methods=['GET'])
def write_socketio_test():
    """Emits a websocket message to check everything is working as it should."""
    socketio.emit('test event', 'test message')
    return jsonify(result=True)


@write.route('/write/validate', methods=['POST'])
def validate_write_parameters():
    return jsonify(result=True)


@write.route('/write/', methods=['POST'])
def start_write():
    # socketio.emit('write', 'test')
    write_func('C:/Users/m/Desktop/test file.mp4')
    return jsonify(result=True)

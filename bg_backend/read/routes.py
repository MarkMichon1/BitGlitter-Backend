from flask import Blueprint, jsonify, request

read = Blueprint('read', __name__)


@read.route('/read/', methods=['POST'])
def start_read():
    # run read with parameters
    return jsonify(test='123')


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
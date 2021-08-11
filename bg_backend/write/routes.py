from flask import Blueprint, jsonify, request

write = Blueprint('write', __name__)


@write.route('/write/validate', methods=['POST'])
def validate_write_parameters():
    return jsonify(result=True)


@write.route('/write/', methods=['POST'])
def start_write():
    return jsonify(result=True)

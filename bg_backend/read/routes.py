from flask import Blueprint, jsonify, request

read = Blueprint('read', __name__)


@read.route('/read/test', methods=['GET'])
def test():
    return jsonify(test='123')

from flask import Blueprint, jsonify, request

config = Blueprint('config', __name__)


@config.route('/config/test', methods=['GET'])
def test():
    return jsonify(test='123')

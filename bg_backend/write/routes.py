from flask import Blueprint, jsonify, request

write = Blueprint('write', __name__)


@write.route('/write/test', methods=['GET'])
def test():
    return jsonify(test='123')

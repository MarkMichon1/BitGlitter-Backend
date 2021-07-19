from flask import Blueprint, jsonify, request

presets = Blueprint('presets', __name__)


@presets.route('/presets/test', methods=['GET'])
def test():
    return jsonify(test='123')

from flask import Blueprint, jsonify, request

presets = Blueprint('presets', __name__)


@presets.route('/presets/validate', methods=['POST'])
def validate_preset_parameters():
    return jsonify(result=True)


@presets.route('/presets', methods=['GET'])
def get_presets():
    return jsonify(test='123')


@presets.route('/presets/add', methods=['POST'])
def add_preset():
    return jsonify(results=True)


@presets.route('/presets/edit', methods=['POST'])
def edit_preset():
    return jsonify(results=True)


@presets.route('/presets/id/7/remove', methods=['GET'])
def remove_preset():
    return jsonify(results=True)

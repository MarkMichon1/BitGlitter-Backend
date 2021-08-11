from flask import Blueprint, jsonify, request

palettes = Blueprint('palettes', __name__)


@palettes.route('/palettes/', methods=['GET'])
def return_all_palettes():
    return jsonify({'someList': ['1', '2', '3']})


@palettes.route('/palettes/id/7/add', methods=['POST'])
def add_palette():
    return jsonify({'palette': 'data'})


@palettes.route('/palettes/id/7/remove', methods=['POST'])
def remove_palette():
    return jsonify({'result': True})


@palettes.route('/palettes/color-distance', methods=['GET'])
def get_color_distance():
    return jsonify({'distance': 7.21})


@palettes.route('/palettes/id/7/set-nickname', methods=['POST'])
def set_nickname():
    return jsonify({'result': True})


@palettes.route('/palettes/base64/verify', methods=['GET'])
def base64_verify():
    return jsonify(valid=False)


@palettes.route('/palettes/base64/export', methods=['GET'])
def base64_export():
    return jsonify(b64_string='')


@palettes.route('/palettes/base64/import', methods=['POST'])
def base64_import():
    return jsonify(b64_string='')


from flask import Blueprint, jsonify, request

palettes = Blueprint('palettes', __name__)


@palettes.route('/palettes/base64/verify', methods=['GET'])
def base64_verify():
    return jsonify(valid=False)


@palettes.route('/palettes/base64/export', methods=['GET'])
def base64_export():
    return jsonify(b64_string='')


@palettes.route('/palettes/base64/import', methods=['GET'])
def base64_import():
    return jsonify(b64_string='')


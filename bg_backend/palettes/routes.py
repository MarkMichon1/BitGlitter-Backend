from flask import Blueprint, jsonify, request

from bg_backend.bitglitter.config.palettefunctions import add_custom_palette, app_validate_palette_values, \
    export_palette_base64, import_palette_base64, remove_custom_palette, return_all_palettes, validate_base64_string
from bg_backend.bitglitter.utilities.palette import get_color_distance

palettes = Blueprint('palettes', __name__)


@palettes.route('/palettes/', methods=['GET', 'POST'])
def return_all_palettes_():
    palette_list = return_all_palettes()
    returned_palette_list = []
    for palette in palette_list:
        returned_palette_values = {'palette_id': palette.palette_id, 'name': palette.name, 'description':
                                  palette.description, 'color_set': palette.color_set, 'color_distance':
                                  palette.color_distance, 'number_of_colors': palette.number_of_colors, 'bit_length':
                                  palette.bit_length, 'time_created': palette.time_created, 'is_24_bit':
                                  palette.is_24_bit, 'is_custom': palette.is_custom, 'is_included_with_repo':
                                  palette.is_included_with_repo}

        returned_palette_list.append(returned_palette_values)
    return jsonify(returned_palette_list)


@palettes.route('/palettes/validate', methods=['POST'])
def validate_palette():
    to_dict = request.get_json()
    returned_errors = app_validate_palette_values(to_dict['name'], to_dict['description'], to_dict['color_set'])
    return jsonify(returned_errors)


@palettes.route('/palettes/add', methods=['POST'])
def add_palette():
    to_dict = request.get_json()
    palette = add_custom_palette(to_dict['name'], to_dict['description'], to_dict['color_set'])
    return jsonify({'name': palette.name, 'description': palette.description, 'color_set': palette.color_set,
                    'color_distance': palette.color_distance, 'number_of_colors': palette.number_of_colors,
                    'bit_length': palette.bit_length, 'time_created': palette.time_created, 'is_24_bit':
                        palette.is_24_bit, 'is_custom': palette.is_custom, 'is_included_with_repo':
                        palette.is_included_with_repo, 'palette_id': palette.palette_id})


@palettes.route('/palettes/remove', methods=['POST'])
def remove_palette():
    to_dict = request.get_json()
    remove_custom_palette(to_dict['palette_id'])
    return jsonify({'result': True})


@palettes.route('/palettes/color-distance', methods=['POST'])
def return_color_distance():
    to_dict = request.get_json()
    return jsonify({'distance': get_color_distance(to_dict['color_set'])})


@palettes.route('/palettes/base64/verify', methods=['GET'])
def base64_verify():
    to_dict = request.get_json()
    return jsonify(validate_base64_string(to_dict['b64_string']))


@palettes.route('/palettes/base64/export', methods=['GET'])
def base64_export():
    to_dict = request.get_json()
    return jsonify(b64_string=export_palette_base64(to_dict['palette_id']))


@palettes.route('/palettes/base64/import', methods=['POST'])
def base64_import():
    to_dict = request.get_json()
    palette = import_palette_base64(to_dict['b64_string'])
    return jsonify({'name': palette.name, 'description': palette.description, 'color_set': palette.color_set,
                    'color_distance': palette.color_distance, 'number_of_colors': palette.number_of_colors,
                    'bit_length': palette.bit_length, 'time_created': palette.time_created, 'is_24_bit':
                    palette.is_24_bit, 'is_custom': palette.is_custom, 'is_included_with_repo':
                    palette.is_included_with_repo, 'palette_id': palette.palette_id})

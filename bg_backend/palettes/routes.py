from flask import Blueprint, jsonify, request

from bg_backend.bitglitter.config.palettefunctions import add_custom_palette, app_validate_palette_values,\
    return_all_palettes

palettes = Blueprint('palettes', __name__)


@palettes.route('/palettes/', methods=['GET', 'POST'])
def return_all_palettes_():
    palette_list = return_all_palettes()
    returned_palette_list = []
    for palette in palette_list:
        returned_palette_values = {}
        returned_palette_values['palette_id'] = palette.palette_id
        returned_palette_values['name'] = palette.name
        returned_palette_values['description'] = palette.description
        returned_palette_values['color_set'] = palette.color_set
        returned_palette_values['color_distance'] = palette.color_distance
        returned_palette_values['number_of_colors'] = palette.number_of_colors
        returned_palette_values['bit_length'] = palette.bit_length
        returned_palette_values['time_created'] = palette.time_created
        returned_palette_values['is_24_bit'] = palette.is_24_bit
        returned_palette_values['is_custom'] = palette.is_custom
        returned_palette_values['is_included_with_repo'] = palette.is_included_with_repo
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


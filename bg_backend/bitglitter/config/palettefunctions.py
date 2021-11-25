import ast
import base64
import logging

from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.palettemodels import Palette
from bg_backend.bitglitter.utilities.palette import get_palette_id_from_hash
from bg_backend.bitglitter.validation.validatepalette import base64_values_validate, custom_palette_values_validate


def _return_palette(palette_id):
    return session.query(Palette).filter(Palette.palette_id == palette_id).first()


def add_custom_palette(palette_name, palette_description, color_set):
    palette_description = palette_description if palette_description else '--'
    new_palette = Palette.create(name=palette_name, description=palette_description, color_set=color_set)
    return new_palette


def remove_custom_palette(palette_id):
    """Removes custom palette completely from the database."""

    palette = _return_palette(palette_id)
    palette.delete()


def return_all_palettes():
    returned_list = session.query(Palette).all()
    return returned_list


def remove_all_custom_palettes():
    """Removes all custom palettes from the database."""
    session.query(Palette).filter(Palette.is_custom).delete()


def validate_base64_string(base64_string):

    try:  # Is it a valid b64 string, and are all required parts included in it?
        decoded_string = base64.b64decode(base64_string.encode()).decode()
        returned_list = decoded_string.split('\\\\')
        palette_id = returned_list[0]
        palette_name = returned_list[1]
        palette_description = returned_list[2]
        time_created = returned_list[3]
        color_set_str = returned_list[4]
        invalid_characters = returned_list[5]
        if invalid_characters != '':
            return {'error': 'invalid'}
    except:
        return {'error': 'invalid'}
    calculated_hash = get_palette_id_from_hash(palette_name, palette_description, time_created, color_set_str)
    if calculated_hash != palette_id:
        return {'error': 'invalid'}

    palette = session.query(Palette).filter(Palette.palette_id == palette_id).first()
    if palette:
        return {'error': 'exists'}
    palette = session.query(Palette).filter(Palette.name == palette_name).first()
    if palette:
        return {'error': 'name'}

    color_set_list = ast.literal_eval(color_set_str)
    results = base64_values_validate(palette_name, palette_description, color_set_list)
    if results:
        return {'error': 'invalid2'}  # Only triggers if someone is messing with the code and trying to break it
    return {}


def import_palette_base64(base64_string):
    decoded_string = base64.b64decode(base64_string.encode()).decode()
    returned_list = decoded_string.split('\\\\')
    palette_id = returned_list[0]
    palette_name = returned_list[1]
    palette_description = returned_list[2]
    time_created = returned_list[3]
    color_set_str = returned_list[4]

    color_set_list = ast.literal_eval(color_set_str)
    palette = Palette.create(palette_id=palette_id, name=palette_name, description=palette_description,
                             time_created=time_created, color_set=color_set_list)

    return palette


def import_custom_palette_from_header(palette_id, stream_header_palette_id, palette_name, palette_description,
                                      time_created, number_of_colors, color_list):
    """Validates values, and creates and returns palette."""
    if palette_id != stream_header_palette_id:
        logging.warning('Corrupted data in palette header, cannot continue.  Aborting...')
        return False

    calculated_id = get_palette_id_from_hash(palette_name, palette_description, time_created, str(color_list))
    if calculated_id != stream_header_palette_id:
        logging.warning('Calculated palette ID / Stream header palette ID mismatch, cannot continue.  Aborting...')
        return False

    if custom_palette_values_validate(palette_name, palette_description, color_list) == False or \
            len(color_list) != number_of_colors:
        logging.warning('Corrupted palette header values, cannot continue.  Aborting...')
        return False

    palette = Palette.create(palette_id=palette_id, is_valid=True, is_custom=True, name=palette_name,
                             description=palette_description, time_created=time_created, color_set=color_list)
    return {'palette': palette}

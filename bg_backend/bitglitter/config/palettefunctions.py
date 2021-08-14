import ast
import base64

from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.palettemodels import Palette
from bg_backend.bitglitter.utilities.palette import get_palette_id_from_hash, render_sample_frame
from bg_backend.bitglitter.validation.validatepalette import custom_palette_values_format_validate


def _return_palette(palette_id):
    return session.query(Palette).filter(Palette.palette_id == palette_id).first()


def add_custom_palette(palette_name, palette_description, color_set):

    new_palette = Palette.create(name=palette_name, palette_id='TEMP', description=palette_description,
                                 color_set=color_set)
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


def generate_sample_frame(path, palette_id=None, all_palettes=False, include_default=False):
    """Prints a small sample frame of a given palette to give an idea of its appearance in normal rendering, selecting
    random colors from the palette for each of the blocks.  Alternatively, if all_palettes=True, all palettes in the
    database will be generated.  Argument include_default toggles whether default palettes are included as well.
    """

    if not all_palettes:
        palette = _return_palette(palette_id=palette_id)
        render_sample_frame(palette.name, palette.convert_colors_to_tuple(), palette.is_24_bit, path)
    else:
        if include_default:
            palettes = session.query(Palette).all()
        else:
            palettes = session.query(Palette).filter(Palette.is_custom)
        for palette in palettes:
            render_sample_frame(palette.name, palette.convert_colors_to_tuple(), palette.is_24_bit, path)


def validate_base64_string(base64_string):

    try:  # Is it a valid b64 string, and are all required parts included in it?
        decoded_string = base64.b64decode(base64_string.encode()).decode()
        palette_id, palette_name, palette_description, time_created, color_set_str = decoded_string.split('\\\\')
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
    results = custom_palette_values_format_validate(palette_name, palette_description, color_set_list)
    if results['name'] or results['description'] or results['color_set']:
        return {'error': 'invalid2'}  # Only triggers if someone is messing with the code and trying to break it
    return {}


def import_palette_base64(base64_string):
    decoded_string = base64.b64decode(base64_string.encode()).decode()
    palette_id, palette_name, palette_description, time_created, color_set_str = decoded_string.split('\\\\')

    color_set_list = ast.literal_eval(color_set_str)
    palette = Palette.create(palette_id=palette_id, name=palette_name, description=palette_description,
                             time_created=time_created, color_set=color_set_list)

    return palette


def app_validate_palette_values(name, description, color_set):
    returned_errors = {'name': [], 'description': [], 'color_set': []}

    # Checking if palette exists
    if session.query(Palette).filter(Palette.name == name).count():
        returned_errors['name'].append('taken')
    elif not name:
        returned_errors['name'].append('none')

    # Format check
    results = custom_palette_values_format_validate(name, description, color_set)
    returned_errors['name'] += results['name']
    returned_errors['description'] = results['description']
    returned_errors['color_set'] = results['color_set']
    return returned_errors

import ast
import base64
import time

from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.palettemodels import Palette
from bg_backend.bitglitter.utilities.palette import get_palette_id_from_hash, render_sample_frame
from bg_backend.bitglitter.validation.utilities import proper_string_syntax
from bg_backend.bitglitter.validation.validatepalette import custom_palette_values_format_validate


def _return_palette(palette_id=None):
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


def import_palette_base64(base64_string):
    decoded_string = base64.b64decode(base64_string.encode()).decode()
    palette_id, palette_name, palette_description, time_created, color_set_str = decoded_string.split('\\\\')

    # Validating data to ensure no funny business
    calculated_hash = get_palette_id_from_hash(palette_name, palette_description, time_created, color_set_str)
    if calculated_hash != palette_id:
        raise ValueError('Corrupted string.  Please ensure you have the full b64 string and try again.')

    palette = session.query(Palette).filter(Palette.palette_id == palette_id).first()
    if palette:
        raise ValueError('Palette already exists locally!')
    if palette.name == palette_name:
        raise ValueError('Palette with this name already exists.')

    color_set_list = ast.literal_eval(color_set_str)
    custom_palette_values_format_validate(palette_name, palette_description, color_set_list)

    palette = Palette.create(palette_id=palette_id, is_valid=True, is_custom=True, name=palette_name,
                             description=palette_description, time_created=time_created, color_set=color_set_list)

    return palette.id


def export_palette_base64(palette_id=None):
    palette = _return_palette(palette_id=palette_id)
    if not palette.is_valid:
        raise ValueError('Cannot export invalid palettes')

    assembled_string = '\\\\'.join([palette.palette_id, palette.name, palette.description, str(palette.time_created),
                                    str(palette.convert_colors_to_tuple())])
    return base64.b64encode(assembled_string.encode()).decode()


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
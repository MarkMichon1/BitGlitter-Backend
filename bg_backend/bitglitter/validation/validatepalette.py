from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.palettemodels import Palette
from bg_backend.bitglitter.utilities.palette import get_color_distance
from bg_backend.bitglitter.validation.utilities import proper_string_syntax


def palette_geometry_verify(stream_palette_bit_length, block_width, block_height, output_type, fps=0):
    """This function calculates the necessary overhead for both images and videos for subsequent frames after 1.  It
    returns a number between 0-100%, for what percentage the overhead occupies.  The lower the value, the higher the
    frame efficiency.
    """

    total_blocks = block_width * block_height

    INITIALIZER_OVERHEAD = block_height + block_width + 579
    FRAME_HEADER_BITS = 352
    occupied_blocks = 0

    if output_type == 'image':
        total_blocks -= INITIALIZER_OVERHEAD
        occupied_blocks += INITIALIZER_OVERHEAD
    bits_available_per_frame = (total_blocks * stream_palette_bit_length) - FRAME_HEADER_BITS
    occupied_blocks += int(FRAME_HEADER_BITS / stream_palette_bit_length)

    payload_frame_percentage = round((((total_blocks - occupied_blocks) / total_blocks) * 100), 2)

    output_per_sec = 0
    if output_type == 'video':
        output_per_sec = bits_available_per_frame * fps

    return payload_frame_percentage, bits_available_per_frame, output_per_sec


def custom_palette_name_validate(name_string):
    if not name_string:
        return 'none'
    if len(name_string) > 50:
        return 'max_length'
    if not proper_string_syntax(name_string):
        return 'ascii'
    if session.query(Palette).filter(Palette.name == name_string).count():
        return 'taken'


def custom_palette_description_validate(description_string):
    if not proper_string_syntax(description_string):
        return 'ascii'
    if len(description_string) > 100:
        return 'max_length'


def custom_palette_color_set_validate(color_set):

    if len(color_set) > 256:
        return 'max_length'

    # Verifying color set parameters.  2^n length, 3 values per color, values are type int, values are 0-255.
    if len(color_set) % 2 != 0 or len(color_set) < 2:
        return '2^n'

    for color_tuple in color_set:
        if len(color_tuple) != 3:
            return 'channels'
        for color in color_tuple:
            if not isinstance(color, int) or color < 0 or color > 255:
                return 'range'

    # Finally, verify colors aren't overlapping (ie, the same color is used twice).
    min_distance = get_color_distance(color_set)
    if min_distance == 0:
        return 'distance'

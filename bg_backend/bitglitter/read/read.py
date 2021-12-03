import logging
from pathlib import Path

from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.configmodels import Config, Constants
from bg_backend.bitglitter.read.process_state.framereadhandler import frame_read_handler
from bg_backend.bitglitter.utilities.filemanipulation import refresh_directory, remove_working_folder
from bg_backend.bitglitter.utilities.loggingset import logging_setter
from bg_backend.bitglitter.utilities.gui.messages import read_done_http
from bg_backend.bitglitter.utilities.read import flush_inactive_frames


def read(file_path,
         input_type,  # App specific
         stop_at_metadata_load=True,
         auto_unpackage_stream=True,
         auto_delete_finished_stream=True,
         output_directory=None,
         bad_frame_strikes=25,
         max_cpu_cores=0,

         # Overrides
         block_height_override=False,
         block_width_override=False,

         # Crypto Input
         decryption_key=None,
         scrypt_n=14,
         scrypt_r=8,
         scrypt_p=1,

         # Logging Settings
         logging_level='info',
         logging_screen_output=True,
         logging_save_output=False,

         # Session Data
         save_statistics=False
         ):
    """This is the high level function that decodes BitGlitter encoded images and video back into the files/folders
    contained within them.  This along with write() are the two primary functions of this library.
    """

    config = session.query(Config).first()
    constants = session.query(Constants).first()

    valid_image_formats = constants.return_valid_image_formats(glob_format=True)

    # Cleanup from previous session if crash:
    flush_inactive_frames()

    # This sets the name of the temporary folder while screened data from partial saves is being written.
    working_directory = Path(constants.WORKING_DIR)
    refresh_directory(working_directory)

    # Setting save path for stream
    if output_directory:
        output_directory = output_directory
    else:
        output_directory = config.read_path
        refresh_directory(config.read_path, delete=False)

    # Logging initializing.
    logging_setter(logging_level, logging_screen_output, logging_save_output, Path(config.log_txt_dir))
    logging.info('Starting read...')

    # Pull valid frame data from the inputted file.
    frame_read_results = frame_read_handler(file_path, output_directory, input_type, bad_frame_strikes, max_cpu_cores,
                                            block_height_override, block_width_override, decryption_key, scrypt_n,
                                            scrypt_r, scrypt_p, working_directory, stop_at_metadata_load,
                                            auto_unpackage_stream, auto_delete_finished_stream, save_statistics,
                                            valid_image_formats)

    # Removing temporary directory
    remove_working_folder(working_directory)

    # Return metadata if conditions are met
    if 'metadata' in frame_read_results:
        return frame_read_results['metadata']

    logging.info('Read cycle complete.')
    read_done_http()
    return frame_read_results

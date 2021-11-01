from pathlib import Path

from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.configmodels import Config, Constants
from bg_backend.bitglitter.utilities.filemanipulation import remove_working_folder
from bg_backend.bitglitter.utilities.gui.messages import write_done_http
from bg_backend.bitglitter.utilities.loggingset import logging_setter
from bg_backend.bitglitter.write.preprocess.preprocessor import PreProcessor
from bg_backend.bitglitter.write.render.renderhandler import RenderHandler
from bg_backend.bitglitter.write.render.videorender import render_video


def write(

        # Basic setup
        input_path,
        # preset_nickname=None,
        stream_name="",
        stream_description="",
        output_directory=None,
        output_mode="video",
        stream_name_file_output=False,
        max_cpu_cores=0,

        # Stream configuration
        compression_enabled=True,
        # error_correction=False, -> to be implemented
        file_mask_enabled=False,

        # Encryption
        encryption_key="",
        scrypt_n=14,
        scrypt_r=8,
        scrypt_p=1,

        # Stream geometry, color, general config
        stream_palette_id='6',
        # stream_palette_nickname=None,
        pixel_width=24,
        block_height=45,
        block_width=80,

        # Video rendering
        frames_per_second=30,

        # Logging
        logging_level='info',
        logging_stdout_output=True,
        logging_txt_output=False,

        # Session Data
        save_statistics=False,

        # App
        bg_version='1.0.0'
):
    """This is the primary function in creating BitGlitter streams from files.  Please see Wiki page or project README
    for more information.
    """

    config = session.query(Config).first() #<--- only used for logging, see below
    constants = session.query(Constants).first()

    # ** Disabled until used by app **
    # Initializing logging, must be up front for logging to work properly.
    logging_setter(logging_level, logging_stdout_output, logging_txt_output, Path(config.log_txt_dir))

    # This sets the name of the temporary folder while the file is being written, as well as the default output path.
    working_dir = Path(constants.WRITE_WORKING_DIR)
    default_output_path = Path(constants.DEFAULT_OUTPUT_DIR)

    # This is what takes the raw input files and runs them through several processes in preparation for rendering.
    pre_processor = PreProcessor(working_dir, input_path, encryption_key, compression_enabled, scrypt_n, scrypt_r,
                                 scrypt_p)

    # This is where the final steps leading up to rendering as well as rendering itself takes place.
    render_handler = RenderHandler(stream_name, stream_description, working_dir, default_output_path, encryption_key,
                                   scrypt_n, scrypt_r, scrypt_p, block_height, block_width, pixel_width,
                                   stream_palette_id, max_cpu_cores, pre_processor.stream_sha256,
                                   pre_processor.size_in_bytes, compression_enabled, pre_processor.encryption_enabled,
                                   file_mask_enabled, pre_processor.datetime_started, bg_version,
                                   pre_processor.manifest, constants.PROTOCOL_VERSION, output_mode, output_directory,
                                   stream_name_file_output, save_statistics)

    # Video render
    if output_mode == 'video':
        render_video(output_directory, default_output_path, stream_name_file_output, working_dir,
                     render_handler.total_frames, frames_per_second, pre_processor.stream_sha256, block_width,
                     block_height, pixel_width, stream_name, render_handler.total_operations)

    # Removing temporary files
    remove_working_folder(working_dir)

    write_done_http()
    return pre_processor.stream_sha256

from sqlalchemy.exc import NoForeignKeysError

from pathlib import Path
import os
import shutil

from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.configmodels import Config, Constants, Statistics
from bg_backend.bitglitter.config.defaultdbdata import load_default_db_data
from bg_backend.bitglitter.config.palettemodels import Palette
from bg_backend.bitglitter.config.presetmodels import Preset
from bg_backend.bitglitter.config.readmodels.streamread import StreamRead
from bg_backend.bitglitter.config.readmodels.readmodels import StreamDataProgress, StreamFile, StreamFrame, \
    StreamSHA256Blacklist


def remove_session():
    """Resets persistent data to factory default settings."""
    model_list = [Config, Constants, Palette, Preset, Statistics, StreamDataProgress, StreamFile, StreamFrame,
                  StreamRead, StreamSHA256Blacklist]
    for model in model_list:
        session.query(model).delete()
    session.commit()
    load_default_db_data()


def return_settings():
    config = session.query(Config).first()
    return {'decoded_files_output_dir': config.read_path, 'read_bad_frame_strikes': config.read_bad_frame_strikes,
            'enable_bad_frame_strikes': config.enable_bad_frame_strikes, 'write_path': config.write_path,
            'maximum_cpu_cores': config.maximum_cpu_cores, 'save_statistics': config.save_statistics,
            'output_stream_title': config.output_stream_title, 'MAX_SUPPORTED_CPU_CORES':
            config.MAX_SUPPORTED_CPU_CORES, 'display_advanced_data': config.display_advanced_data}


def update_settings(read_path, read_bad_frame_strikes, enable_bad_frame_strikes, write_path,
                    maximum_cpu_cores, save_statistics, output_stream_title, display_advanced_data):
    config = session.query(Config).first()
    config.read_path = read_path
    config.read_bad_frame_strikes = read_bad_frame_strikes
    config.enable_bad_frame_strikes = enable_bad_frame_strikes
    config.write_path = write_path
    # config.log_txt_path = log_txt_path
    # config.log_output = log_output
    # config.logging_level = logging_level
    config.maximum_cpu_cores = maximum_cpu_cores
    config.save_statistics = save_statistics
    config.output_stream_title = output_stream_title
    config.display_advanced_data = display_advanced_data
    config.save()


def output_stats():
    """Returns a dictionary object containing read and write statistics."""
    stats = session.query(Statistics).first()
    return stats.return_stats()


def clear_stats():
    """Resets all write and read values back to zero."""
    stats = session.query(Statistics).first()
    stats.clear_stats()


def write_stats_update(blocks, frames, data):
    """Internal function to update stats after rendering completes, along with read update below."""
    stats = session.query(Statistics).first()
    stats.write_update(blocks, frames, data)


def read_stats_update(blocks, frames, data):
    stats = session.query(Statistics).first()
    stats.read_update(blocks, frames, data)


def read_warmup():
    """Loads config settings used in read()"""
    config = session.query(Config).first()
    return {'read_path': config.read_path, 'strikes_enabled': config.enable_bad_frame_strikes, 'strike_count':
        config.read_bad_frame_strikes, 'cpu_cores': config.maximum_cpu_cores}


def write_warmup():
    """Loads config settings used in write()"""
    config = session.query(Config).first()
    return {'cpu_cores': config.maximum_cpu_cores, 'output_stream_title': config.output_stream_title,
            'save_statistics': config.save_statistics, 'write_path': config.write_path}


def remove_render_directory():
    """Ran at startup and when write() fails."""
    try:
        constants = session.query(Constants).first()
        temp_render_path = Path(constants.WORKING_DIR)
        if temp_render_path.exists():
            shutil.rmtree(temp_render_path)
    except NoForeignKeysError:
        pass


def backend_startup():
    """Deletes temporary folder for write (if it exists) and creates directories for read path and write path if they
    don't already exist.
    """
    # Render path
    remove_render_directory()

    config = session.query(Config).first()
    # Read path
    read_path = Path(config.read_path)
    if not read_path.exists():
        os.makedirs(read_path)
    # Write path
    write_path = Path(config.write_path)
    if not write_path.exists():
        os.makedirs(write_path)

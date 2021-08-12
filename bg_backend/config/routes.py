from flask import Blueprint, jsonify, request

from bg_backend.bitglitter.config.configfunctions import clear_stats, output_stats, return_settings, update_settings
from bg_backend.bitglitter.utilities.display import humanize_file_size, humanize_integer_comma

config = Blueprint('config', __name__)


@config.route('/config/clear-session', methods=['GET'])
def clear_session():
    """Resets persistent data to factory default settings."""
    # clear entire db, load default settings
    return jsonify(test='123')


@config.route('/config/statistics', methods=['GET'])
def get_statistics():
    results = output_stats()
    results['data_wrote'] = humanize_file_size(results['data_wrote'])
    results['data_read'] = humanize_file_size(results['data_read'])
    results['blocks_wrote'] = humanize_integer_comma(results['blocks_wrote'])
    results['frames_wrote'] = humanize_integer_comma(results['frames_wrote'])
    results['blocks_read'] = humanize_integer_comma(results['blocks_read'])
    results['frames_read'] = humanize_integer_comma(results['frames_read'])
    return jsonify(results)


@config.route('/config/statistics/reset', methods=['GET'])
def reset_statistics():
    clear_stats()
    return jsonify({'result': True})


@config.route('/config/settings', methods=['GET', 'POST'])
def settings():
    """Get and update settings for app."""
    if request.method == 'GET':
        return jsonify(return_settings())
    elif request.method == 'POST':
        to_dict = request.get_json()
        update_settings(to_dict['decoded_files_output_path'], to_dict['read_bad_frame_strikes'],
                        to_dict['disable_bad_frame_strikes'], to_dict['write_path'], to_dict['log_txt_path'],
                        to_dict['log_output'], to_dict['logging_level'], to_dict['maximum_cpu_cores'],
                        to_dict['save_statistics'], to_dict['output_stream_title'], )
        return jsonify({'result': True})

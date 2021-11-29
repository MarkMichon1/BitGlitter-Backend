from flask import Blueprint, jsonify, request

from bg_backend.bitglitter.config.configfunctions import clear_stats, output_stats, remove_session, return_settings,\
    update_settings

config = Blueprint('config', __name__)


@config.route('/config/test', methods=['GET'])
def test():
    """Test route to make sure things are working as they should with ElectronJS, echoes JSON back.  Keep."""
    return jsonify(request.get_json())


@config.route('/config/clear-session', methods=['GET'])
def clear_session():
    """Resets persistent data to factory default settings."""
    remove_session()
    return jsonify(success=True)


@config.route('/config/statistics', methods=['GET'])
def get_statistics():
    results = output_stats()
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
        if to_dict['save_statistics'] == False:
            clear_stats()
        update_settings(to_dict['read_path'], to_dict['read_bad_frame_strikes'],
                        to_dict['enable_bad_frame_strikes'], to_dict['write_path'], to_dict['maximum_cpu_cores'],
                        to_dict['save_statistics'], to_dict['output_stream_title'], to_dict['display_advanced_data'])
        return jsonify({'result': True})

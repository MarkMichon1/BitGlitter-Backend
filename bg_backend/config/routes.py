from flask import Blueprint, jsonify, request

config = Blueprint('config', __name__)


@config.route('/config/clear-session', methods=['GET'])
def clear_session():
    """Resets persistent data to factory default settings."""
    # clear entire db, load default settings
    return jsonify({'result': True})


@config.route('/config/statistics', methods=['GET'])
def get_statistics():
    return jsonify({'stats': {'1': 1, '2': 2}})


@config.route('/config/statistics/reset', methods=['GET'])
def reset_statistics():
    return jsonify({'result': True})


@config.route('/config', methods=['GET', 'POST'])
def settings():
    """Get and update settings for app."""
    if request.method == 'GET':
        return jsonify({'result': True})
    elif request.method == 'POST':
        return jsonify({'result': True})

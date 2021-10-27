import requests

from config import ELECTRON_EXPRESS_PORT

APP_LOCATION = f'http://localhost:{ELECTRON_EXPRESS_PORT}'


def write_test_http():
    requests.post(f'{APP_LOCATION}/write/test', json={'success': True})


def write_preprocess_http(text):
    requests.post(f'{APP_LOCATION}/write/write-preprocess', json={'text': text})


def write_frame_count_http(total_frames):
    requests.post(f'{APP_LOCATION}/write/frame-count', json={'total_frames': total_frames})


def write_render_http(frame_number, percentage):
    requests.post(f'{APP_LOCATION}/write/write-render', json={'frame_number': frame_number, 'percentage': percentage})


def write_video_render_http(frame_number, percentage):
    requests.post(f'{APP_LOCATION}/write/write-video-render', json={'frame_number': frame_number, 'percentage':
        percentage})


def write_stream_sha_http(stream_sha256):
    requests.post(f'{APP_LOCATION}/write/stream-sha', json={'sha256': stream_sha256})


def write_save_path_http(save_path):
    requests.post(f'{APP_LOCATION}/write/save-path', json={'save_path': save_path})


def write_done_http():
    requests.post(f'{APP_LOCATION}/write/done', json={'done': True})


def write_error_http(traceback, write_path):
    requests.post(f'{APP_LOCATION}/write/error', json={'traceback': traceback, 'write_path': write_path})


####################################################


def read_error_http(traceback, read_path):
    requests.post(f'{APP_LOCATION}/read/error', json={'traceback': traceback, 'read_path': read_path})

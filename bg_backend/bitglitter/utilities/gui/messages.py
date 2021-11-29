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


def read_test_http():
    requests.post(f'{APP_LOCATION}/read/test', json={'success': True})


def read_frame_count_http(total_frames_session):
    requests.post(f'{APP_LOCATION}/read/frame-total', json={'total_frames_session': total_frames_session})


def read_frame_process_http(frame_position):
    requests.post(f'{APP_LOCATION}/read/frame-position', json={'frame_position': frame_position})


def read_stream_sha256_http(stream_sha256):
    requests.post(f'{APP_LOCATION}/read/stream-sha', json={'sha256': stream_sha256})


def read_metadata_http(stream_sha256, stream_name, stream_description, payload_size, total_frames, time_created,
                       is_compressed, is_encrypted, file_mask_enabled, stream_palette_name, block_height, block_width,
                       bg_version, protocol, manifest, manifest_decrypt_success):
    payload = {'stream_sha256': stream_sha256, 'stream_name': stream_name, 'stream_description': stream_description,
               'payload_size': payload_size, 'total_frames': total_frames, 'time_created': time_created,
               'is_compressed': is_compressed, 'is_encrypted': is_encrypted, 'file_mask_enabled': file_mask_enabled,
               'stream_palette_name': stream_palette_name, 'block_height': block_height, 'block_width': block_width,
               'bg_version': bg_version, 'protocol': protocol, 'manifest': manifest, 'manifest_decrypt_success':
               manifest_decrypt_success} #todo verify
    requests.post(f'{APP_LOCATION}/read/metadata', json=payload)


def read_path_http(path):
    requests.post(f'{APP_LOCATION}/read/path', json={'path': path})


def read_done_http():
    requests.post(f'{APP_LOCATION}/read/done', json={'done': True})


def read_hard_error_http(traceback, read_path):
    requests.post(f'{APP_LOCATION}/read/error', json={'traceback': traceback, 'read_path': read_path})


def read_soft_error_http(type_of_error):
    requests.post(f'{APP_LOCATION}/read/error', json={'type_of_error': type_of_error})


def read_total_strikes_http(total_strikes):
    requests.post(f'{APP_LOCATION}/read/total-strikes', json={'total_strikes': total_strikes})


def read_new_strike(count):
    requests.post(f'{APP_LOCATION}/read/total-strikes', json={'count': count})

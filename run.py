import multiprocessing
multiprocessing.freeze_support()

from bg_backend import socketio, web_app

print(f'NEW PROCESS: {__name__}')

if __name__ == '__main__':
    print('main')
    socketio.run(web_app, debug=True, host='127.0.0.1', port=21168, use_reloader=False)
else:
    print('not main')
from bg_backend import socketio, web_app

if __name__ == '__main__':
    socketio.run(web_app, debug=True, host='localhost', port='7218')
    #  todo- remove debug

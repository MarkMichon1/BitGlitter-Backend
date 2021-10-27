from bg_backend import web_app
from config import BACKEND_HOST, BACKEND_PORT

if __name__ == '__main__':
    web_app.run(debug=True, host=BACKEND_HOST, port=BACKEND_PORT, use_reloader=False)

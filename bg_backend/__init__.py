from flask import Flask

web_app = Flask(__name__)

from bg_backend.config.routes import config
from bg_backend.palettes.routes import palettes
from bg_backend.presets.routes import presets
from bg_backend.read.routes import read
from bg_backend.write.routes import write

web_app.register_blueprint(config)
web_app.register_blueprint(palettes)
web_app.register_blueprint(presets)
web_app.register_blueprint(read)
web_app.register_blueprint(write)
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


# ===============================================================================
# The MIT License (MIT)
#
# Copyright (c) 2021 - ∞ Mark Michon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ===============================================================================
#
# Python library project page:
# https://github.com/MarkMichon1/BitGlitter-Python
#
# Electron App project page:
# https://github.com/MarkMichon1/BitGlitter
#
# Discord server:
# https://discord.gg/t9uv2pZ
#
# Enjoy! :)
#
#   - Mark
# ===============================================================================

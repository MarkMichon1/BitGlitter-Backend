![BitGlitter Logo](https://i.imgur.com/pX8b4Dy.png)

### Python Backend For App (you are here) | [Electron Desktop App](https://github.com/MarkMichon1/BitGlitter) | [Python Library](https://github.com/MarkMichon1/BitGlitter-Python)

## Store and transfer files using high-performance animated barcodes ⚡

![BitGlitter Sample GIF](https://i.imgur.com/lPFR5kA.gif) 

**[Discord Server](https://discord.gg/t9uv2pZ)** 

This is the backend for the [BitGlitter desktop app](https://github.com/MarkMichon1/BitGlitter).  Its the 
[original Python library](https://github.com/MarkMichon1/BitGlitter-Python) wrapped in `Flask` and using `requests`
for bidirectional communication between the two.

The original Python library is included inside this repository (rather than be a dependency) because several 
important changes are made to it in order for the library to play nice inside a desktop app.  For more information,
please check out the page for the [desktop app](https://github.com/MarkMichon1/BitGlitter)

This repo is 98% similar to the Python library.  Changes, bugfixes, and improvements performed here will cascade there
(and vice versa).

### Roadmap

Here are a few possible directions this can move in which would increase its usefulness and versatility:
- **"Splash Screen":** At the end of streams, include some cool looking rendered animation with the project logo, a
  brief explanation of what it is, and a URL to download the software.  People not knowing what BitGlitter is will now
  have an idea as well as a way to download it, increasing usage and fueling development of the project.  Could also
  include metadata about the stream itself.
- **Inline streams:** Have a stream embedded in another (non-BitGlitter) video, allowing for data to be read inside of
  a normal, human-friendly video.  Rather than taking up the full video screen, the stream could be a bar on the top or
  bottom of the screen, or any arbitrary shape (perhaps even animated).  This allows content creators to 'attach' files
  to their videos, much like you can attach arbitrary files to an email.
- **Moving heavy lifting away from Python:** While libraries like `cv2` and `numpy` are used which utilize C++, pure
  Python is used in a few heavily used functions (thousands of times per second).  Moving these to Rust or C++ would
  substantially speed up the software, and make new use cases possible...
- **Livestream capabilities:** BitGlitter streams can be 'broadcast' over live video.  Reader would be able to detect
  data streams through visual or audio cues from the multimedia, and can process/decode on the fly.  BitGlitter streams
  are no longer restricted to 'static' files, but are open to any kind of live-streaming data, which can be optionally
  compressed/encrypted through the original feature set.

### Contributing

**Let me know of your ideas and suggestions!**  There are many directions this technology can go in, and with enough interest
your ideas can be future additions to this core library (as well as the desktop app).  If you're looking to help with
developing it.... awesome.  All I ask is you're skilled with Python, and can write clean and structured code.  I went
out of my way to have clear variable and function names as well as a decent amount of comments scattered throughout the
library- it should be relatively easy to get up to speed to understand how BitGlitter works underneath the hood.

Drop in and say hi on the Discord server:

**https://discord.gg/t9uv2pZ**

# MIT License

© 2021 - ∞ Mark Michon

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
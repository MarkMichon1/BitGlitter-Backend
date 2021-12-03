from setuptools import setup, find_namespace_packages

with open("README.md", "r") as openReadMe:
    long_description = openReadMe.read()

setup(
    name="BitGlitter Backend",
    version="1.0.0",
    author="Mark Michon",
    author_email="markkmichon@gmail.com",
    description="⚡ This is the backend for the BitGlitter desktop app. Its the original Python library wrapped in Flask"
                " and using requests for bidirectional communication between the two.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarkMichon1/BitGlitter-Backend",
    packages=find_namespace_packages(),
    install_requires=[
        "bitstring==3.1.9",
        "cryptography==3.4.8",
        "Flask==2.0.1",
        "Flask-SocketIO==5.1.1",
        "opencv-python==4.5.3.56",
        "requests==2.26.0",
        "SQLAlchemy==1.4.25"
    ],
    extra_require={"dev": "pytest"},
    classifiers=[
        "Programming Language :: Python :: 3.9.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

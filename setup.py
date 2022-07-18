from setuptools import setup

setup(
    name='image-server',
    version="1.0.0",
    py_modules=['image_server'],
    entry_points = {
        'console_scripts': ['image-server = image_server:start']},
    install_requires=[
        "foxglove-websocket>=0.0.7"
    ]
)

import base64
from functools import partial
import json
import os
import time
import click
from lemon import entrypoint
from lemon.api import subscribe
from foxglove_websocket.server import FoxgloveServer
import numpy as np

def to_raw_image(img: "np.ndarray", timestamp):
    encoding = 'mono8' if len(img.shape) < 3 else 'rgb8'
    return json.dumps({
        **timestamp,
        'width': img.shape[1],
        'height': img.shape[0],
        'encoding': encoding,
        'step': 1,
        'data': base64.b64encode(img.astype(np.uint8)).decode('utf-8')
    }).encode('utf-8')


@click.argument('topics', nargs=-1)
@entrypoint
async def start(topics):
    async with FoxgloveServer("127.0.0.1", 8765, "Image Server for Lemon 🍋") as server:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/RawImage.json', 'r') as f:
            schema = json.dumps(json.load(f))
            channels = {
                topic: await server.add_channel({
                    "topic": topic,
                    "encoding": "json",
                    "schemaName": "foxglove.RawImage",
                    "schema": schema
                }) for topic in topics}

        async def send(topic, msg):
            channel = channels[topic]
            await server.send_message(channel, time.time_ns(), to_raw_image(*msg))

        await subscribe({topic: partial(send, topic) for topic in topics})

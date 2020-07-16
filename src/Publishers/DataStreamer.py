import websockets
import  asyncio
import json

from src.ConfigLoader import ConfigBase


class Streamer(ConfigBase):
    def __init__(self):
        super().__init__("stream")


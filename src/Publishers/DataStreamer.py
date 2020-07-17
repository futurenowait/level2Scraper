import websockets
import zmq
import asyncio
import json


from src.ConfigLoader import ConfigBase
from src.ZeroMQ.ZeroMq_Handlers import Publisher

class Stream(ConfigBase):
    def __init__(self,exchange):
        super().__init__("stream",exchange)
        self._connect_to_zeromq()

    def _connect_to_zeromq(self):
        self._publisher = Publisher()

    def _handle_data(self):
        def publish_data(data):
            pass

        pass

    async def _listen(self):
        pass

class BitmexStream(Stream):
    def __init__(self):

        super().__init__("bitmex")
        self._build_wss_commands()
        self._connect_to_zeromq()

    def _build_wss_commands(self):

        command_template = {"op":"subscribe","args":[]}

        if type(self._symbols) is list:
            for symbol in self._symbols:
                command_template['args'].append("trade:{}".format(symbol))
        else:
            command_template['args'].append("trade:{}".format(self._symbols))

        self._wss_command = command_template

    def _handle_data(self):
        pass

    async def listen(self):
        pass


### Not Implemented
class BinanceStream(Stream):
    def __init__(self):
        super().__init__("binance")

        #self._build_wss_commands()
        self._connect_to_zeromq()
        self._listen()

    def _handle_data(self):
        pass

    async def _callback(self):
        pass

    async def _listen(self):
        pass

### Not Implemented
class DeribitStream(Stream):
    def __init__(self):
        super().__init__("deribit")

        # self._build_wss_commands()
        self._connect_to_zeromq()
        self._listen()

    def _handle_data(self):
        pass

    async def _callback(self):
        pass

    async def _listen(self):
        pass


ss = BitmexStream()
asyncio.get_event_loop().run_until_complete(ss.listen())
print()
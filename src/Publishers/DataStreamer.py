import websockets
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

    def _build_wss_commands(self):

        command_template = {"op":"subscribe","args":[]}

        if type(self._symbols) is list:
            for symbol in self._symbols:
                command_template['args'].append("trade:{}".format(symbol))
        else:
            command_template['args'].append("trade:{}".format(self._symbols))

        self._wss_command = command_template

    async def listen(self):

        async with websockets.connect(self._url) as websocket:
            try:
                while True:
                    message = await websocket.recv()
                    message = json.loads(message)

                    if 'info' in message:
                        print(message)
                        await websocket.send(json.dumps(self._wss_command))

                    elif 'table' in message:
                        if message['action'] == "insert":

                            if 'trade' == message['table']:
                                self._publisher._send(message['data'],"trade.bitmex")


            except Exception as error:
                print(error)


### Not Implemented
class BinanceStream(Stream):
    def __init__(self):
        super().__init__("binance")

        #self._build_wss_commands()

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

    def _handle_data(self):
        pass

    async def _callback(self):
        pass

    async def _listen(self):
        pass


ss = BitmexStream()
asyncio.get_event_loop().run_until_complete(ss.listen())

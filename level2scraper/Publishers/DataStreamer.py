import websockets
import asyncio
import json


from level2scraper.ConfigLoader import ConfigBase
from level2scraper.ZeroMQ.ZeroMq_Handlers import Publisher


class Stream(ConfigBase):
    def __init__(self,exchange):
        """
        Base Object for Streamers. Inherits variables from ConfigBase that we construct using stream type. Then
        runs ZeroMQ messaging channel

        :type exchange: string
        :param exchange: Used for loading correct configuration to object
        """
        super().__init__("stream",exchange)
        self._connect_to_zeromq()

    def _connect_to_zeromq(self):
        """
        Initializing Publisher type of ZeroMQ client. Which will push data to subscribers. In our case to Data Processors
        :return:
        """
        self._publisher = Publisher()


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
                        await websocket.send(json.dumps(self._wss_command))

                    elif 'table' in message:
                        if message['action'] == "insert":

                            if 'trade' == message['table']:
                                self._publisher.send(message['data'], "trade.bitmex")

            except Exception as error:
                print(error)


ss = BitmexStream()
asyncio.get_event_loop().run_until_complete(ss.listen())

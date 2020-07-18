import websockets
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
                        """
                        Message looks like:
                        {'info': 'Welcome to the BitMEX Realtime API.', 
                        'version': '2020-07-14T21:30:54.000Z', 
                        'timestamp': '2020-07-18T07:57:52.984Z', 
                        'docs': 'https://www.bitmex.com/app/wsAPI', 
                        'limit': {'remaining': 38}
                        }
                        """
                        print(message['info'])
                        await websocket.send(json.dumps(self._wss_command))

                    elif 'table' in message:
                        if message['action'] == "insert":

                            if 'trade' == message['table']:
                                """
                                Message Looks Like:
                                {'table': 'trade', 
                                'action': 'insert', 
                                'data': [
                                    {'timestamp': '2020-07-18T08:01:48.052Z', 
                                    'symbol': 'XBTUSD', 
                                    'side': 'Sell', 
                                    'size': 500, 
                                    'price': 9136, 
                                    'tickDirection': 'ZeroMinusTick', 
                                    'trdMatchID': '00b2e350-d4de-89e1-23cb-d1be234af252', 
                                    'grossValue': 5473000, 
                                    'homeNotional': 0.05473, 
                                    'foreignNotional': 500}
                                    ]
                                }

                                """
                                self._publisher.send(message['data'], "trade.bitmex")

            except Exception as error:
                print(error)

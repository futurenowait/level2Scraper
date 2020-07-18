import asyncio

from level2scraper.ConfigLoader import ConfigBase
from level2scraper.ZeroMQ.ZeroMq_Handlers import Subscriber
from level2scraper.Subscribers.Bitmex.DataObject import BitmexDataStructure

class Processor(ConfigBase):
    """
    Object for future scalability purposes
    """
    def __init__(self,exchange):
        super().__init__("process",exchange)


class BitmexDataProcessor(Processor):
    def __init__(self):
        super().__init__("bitmex")
        self._connect_to_zeromq()
        self._data = []
        self._current_symbols = []

    def _connect_to_zeromq(self):
        self._subscriber = Subscriber("trade.bitmex")

    def _handle_data(self,data):
        pass

    async def _listen(self):
        while not self._subscriber.do_close:
            message = self._subscriber.socket.recv_string()
            topic,data = message.split("|")
            if data['symbol'] not in self._current_symbols:
                new_data = BitmexDataStructure(data['symbol'])
                new_data.add_data(data)






bb = BitmexDataProcessor()
asyncio.get_event_loop().run_until_complete(bb._listen())
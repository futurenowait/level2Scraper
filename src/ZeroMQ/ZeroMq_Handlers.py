import zmq

from src.ConfigLoader import ConfigBase


class Publisher(ConfigBase):
    def __init__(self):
        super().__init__("zeromq")
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind("tcp://*:{}".format(self._port))

    def _send(self,data,topic):
        self._socket.send_string("{0} {1}".format(topic, data))

    def _close(self):
        self._socket.close()

class Subscriber(ConfigBase):
    def __init__(self,topic_filter=None):
        super().__init__("zeromq")
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self._socket.connect("tcp://localhost:{}".format(self._port))

        if topic_filter:
            self._socket.setsockopt(zmq.SUBSCRIBE,topic_filter)

        self._do_close = False

    def _close(self):
        self._do_close = True
    async def _listen(self):
        while not self._do_close:
            message = self._socket.recv_string()
            topic, data = message.split()

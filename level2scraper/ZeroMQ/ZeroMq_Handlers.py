import zmq

from level2scraper.ConfigLoader import ConfigBase


class Publisher(ConfigBase):
    def __init__(self):
        super().__init__("zeromq")
        self._context = zmq.Context()
        self.socket = self._context.socket(zmq.PUB)
        self.socket.bind("tcp://*:{}".format(self._port))

    def send(self, data, topic):
        self.socket.send_string("{0}|{1}".format(topic, data))

    def _close(self):
        self.socket.close()

class Subscriber(ConfigBase):
    def __init__(self,topic_filter=None):
        super().__init__("zeromq")
        self._context = zmq.Context()
        self.socket = self._context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:{}".format(self._port))

        if topic_filter:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic_filter)

        self.do_close = False

    def close(self):
        self.do_close = True

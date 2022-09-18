import json
import logging
import zmq
from .type import StreamData, Event
from .utils import to_stream_data
import logging
logger = logging.getLogger(__name__)

class Server():
    def __init__(self, address="127.0.0.1", port=5556):
        self.address = address
        self.port = port

    def start(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://{}:{}".format(self.address, self.port))

    def stream(self):
        while True:
            # data: {"event": "on_tick", "data": {}}
            res = self.socket.recv_string()
            json_data = json.loads(res)
            stream_data = to_stream_data(json_data)
            yield (stream_data.event, stream_data.data)
            message="ok"
            self.socket.send_string("Reply: %s" % message)
            if stream_data.event == Event.ON_DEINIT:
                break

    def stop(self):
        self.socket.close()
        self.context.destroy()


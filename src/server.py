import json
import logging
import zmq
from type import StreamData, Event

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
            data = json.loads(res)
            res = StreamData(event=Event(data["event"]), data={})
            print("debug: ",res)
            yield (res.event, res.data)
            message="thank you"
            self.socket.send_string("Reply: %s" % message)
            if res.event == Event.ON_DEINIT:
                break

    def stop(self):
        self.socket.close()
        self.context.destroy()


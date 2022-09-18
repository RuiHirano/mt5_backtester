import json
import zmq
import time
import sys
import threading

class APIThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, socket, target=None):
        super(APIThread, self).__init__(target=target)
        self.socket = socket
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self.stopped():
            message = self.socket.recv_string()
            print("Received api = %s" % message)
            self.socket.send_string("Reply: %s" % message)

    def stopped(self):
        return self._stop_event.is_set()

class ExpertAdvisor():
    def __init__(self):
        self.cl_context = zmq.Context()
        self.cl_socket = self.cl_context.socket(zmq.REQ)
        self.cl_socket.connect("tcp://127.0.0.1:5556")
        self.api_context = zmq.Context()
        self.api_socket = self.api_context.socket(zmq.REP)
        self.api_socket.bind("tcp://127.0.0.1:5557")

    def __enter__(self):
        # run server
        print('[backtester] Starting server...')
        self.api_thread = APIThread(socket=self.api_socket)
        self.api_thread.start()
        print('[backtester] Start')
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        # stop server
        print('[backtester] Stopping server...')
        self.api_thread.stop()
        time.sleep(1)
        print('[backtester] Done.')

    def run(self):
        self.on_init()
        for i in range(10):
            self.on_tick()
            time.sleep(0.1)
        self.on_deinit()

    def on_init(self):
        print("===OnInit========")
        #message = sys.stdin.readline()
        data = {"event": "on_init", "data": {}}
        message = json.dumps(data)
        self.cl_socket.send_string(message)

        recv_message = self.cl_socket.recv_string()
        print("Init Finished = %s" % recv_message)

    def on_deinit(self):
        print("===OnDeinit========")
        #message = sys.stdin.readline()
        data = {"event": "on_deinit", "data": {}}
        message = json.dumps(data)
        self.cl_socket.send_string(message)

        recv_message = self.cl_socket.recv_string()
        print("Deinit Finished = %s" % recv_message)

    def on_tick(self):
        print("===OnTick========")
        #message = sys.stdin.readline()
        data = {"event": "on_tick", "data": {}}
        message = json.dumps(data)
        self.cl_socket.send_string(message)

        recv_message = self.cl_socket.recv_string()
        print("Tick Finished = %s" % recv_message)

if __name__ == "__main__":
    with ExpertAdvisor() as ea:
        ea.run()

import json
import zmq
import time
import threading
from .utils import to_api_request
from .type import APIRequestType, AccountInfo, Rate, TradeResult, Tick

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
            data = json.loads(message)
            api_request = to_api_request(data)
            print("Received api = ", api_request)
            if api_request.type == APIRequestType.GET_ACCOUNT_INFO:
                account_info =  AccountInfo(balance=10000, credit=10000, currency="EURUSD", equity=10000, profit=10000, margin=10000, margin_free=10000, margin_level=10000)
                message = json.dumps(account_info._asdict())
                self.socket.send_string(message)
            elif api_request.type == APIRequestType.GET_RATES:
                rates = [Rate(time=123456789, open=1.23456, high=1.23456, low=1.23456, close=1.23456, volume=123, spread=1)]
                message = json.dumps([rate._asdict() for rate in rates])
                self.socket.send_string(message)
            elif api_request.type == APIRequestType.ORDER_SEND:
                result = TradeResult(ticket=123456789, retcode=0)
                message = json.dumps(result._asdict())
                self.socket.send_string(message)
            else:
                message = "Unknown"
                self.socket.send_string(message)

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
        data = {"event": "ON_INIT", "data": {}}
        message = json.dumps(data)
        self.cl_socket.send_string(message)

        recv_message = self.cl_socket.recv_string()
        print("Init Finished = %s" % recv_message)

    def on_deinit(self):
        print("===OnDeinit========")
        #message = sys.stdin.readline()
        data = {"event": "ON_DEINIT", "data": {}}
        message = json.dumps(data)
        self.cl_socket.send_string(message)

        recv_message = self.cl_socket.recv_string()
        print("Deinit Finished = %s" % recv_message)

    def on_tick(self):
        print("===OnTick========")
        #message = sys.stdin.readline()
        tick_dict = Tick(time=123456789, bid=1.23456, ask=1.23456, last=1.223334, volume=233.3)._asdict()
        data = {"event": "ON_TICK", "data": {"tick": tick_dict}}
        message = json.dumps(data)
        self.cl_socket.send_string(message)

        recv_message = self.cl_socket.recv_string()
        print("Tick Finished = %s" % recv_message)

if __name__ == "__main__":
    with ExpertAdvisor() as ea:
        ea.run()

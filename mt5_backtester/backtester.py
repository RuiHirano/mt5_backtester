import logging
from .server import Server
from .api import API
from .type import TradeRequest, Event

class Backtester():
    def __init__(self, level=logging.INFO):
        logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s', level=level)
        self.logger = logging.getLogger(__name__)
        self.server = Server(address="127.0.0.1", port=5556)
        self.api = API(address="127.0.0.1", port=5557)
        self.setup()

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def setup(self):
        # run server
        self.logger.info('[backtester] Starting server...')
        self.server.start()
        self.api.connect()
        self.logger.info('[backtester] Start at {}:{}'.format(self.server.address, self.server.port))

    def close(self):
        # stop server
        self.logger.info('[backtester] Stopping server...')
        self.server.stop()
        self.logger.info('[backtester] Done.')

    def stream(self):
        for (event, data) in self.server.stream():
            yield (event, data)

if __name__ == "__main__":
    with Backtester() as bt:
        for (event, data) in bt.stream():
            if event == Event.ON_INIT:
                pass
            elif event == Event.ON_TICK:
                rates = bt.api.get_rates("EURUSD", "M1", 0, 0)
                print(rates)
                account = bt.api.get_account_info()
                print(account)
                request = TradeRequest(symbol="EURUSD", volume=0.01, type=0, price=0, stoploss=0, takeprofit=0, magic=0, comment="test", expiration=0, slippage=0)
                result = bt.api.order_send(request)
                print(result)
            elif event == Event.ON_DEINIT:
                pass


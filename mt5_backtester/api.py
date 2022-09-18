import json
from typing import List
from .type import APIRequest, APIRequestType, Rate, AccountInfo, TradeRequest, TradeResult
import pandas as pd
import zmq
from .utils import to_account_info, to_trade_result, to_rates
import logging
logger = logging.getLogger(__name__)

class API:
    def __init__(self, address="127.0.0.1", port=5557):
        self.address = address
        self.port = port

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(self.address, self.port))

    def disconnect(self):
        self.socket.close()
        self.context.destroy()

    ####################
    # Time Series API  #
    ####################
    def get_rates(self, symbol, timeframe, start, end, dataframe=True) -> List[Rate]:
        req = APIRequest(type=APIRequestType.GET_RATES, data={})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_rates] = %s" % recv_message)
        json_data = json.loads(recv_message)
        rates = to_rates(json_data)
        #rates = [Rate(time=123456789, open=1.23456, high=1.23456, low=1.23456, close=1.23456, volume=123, spread=1)]
        if dataframe:
            return pd.DataFrame(rates)
        return rates

    ####################
    # Account API      #
    ####################
    def get_account_info(self) -> AccountInfo:
        req = APIRequest(type=APIRequestType.GET_ACCOUNT_INFO, data={})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_account_info] = %s" % recv_message)
        json_data = json.loads(recv_message)
        account_info = to_account_info(json_data)
        #account_info =  AccountInfo(balance=10000, credit=10000, currency="EURUSD", equity=10000, profit=10000, margin=10000, margin_free=10000, margin_level=10000)
        return account_info

    ####################
    # Order API      #
    ####################
    def order_send(self, request: TradeRequest) -> TradeResult:
        req = APIRequest(type=APIRequestType.ORDER_SEND, data=request._asdict())
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[order_send] = %s" % recv_message)
        json_data = json.loads(recv_message)
        result = to_trade_result(json_data)
        return result

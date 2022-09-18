import logging
import re
from typing import List
from type import Rate, AccountInfo, TradeRequest, TradeResult
import pandas as pd
import zmq

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
        self.socket.send_string("get_rates")
        recv_message = self.socket.recv_string()
        print("Receive message = %s" % recv_message)
        rates = [Rate(time=123456789, open=1.23456, high=1.23456, low=1.23456, close=1.23456, volume=123, spread=1)]
        if dataframe:
            return pd.DataFrame(rates)
        return rates

    ####################
    # Account API      #
    ####################
    def get_account_info(self) -> AccountInfo:
        self.socket.send_string("get_account_info")
        recv_message = self.socket.recv_string()
        print("Receive message = %s" % recv_message)
        account_info =  AccountInfo(balance=10000, credit=10000, currency="EURUSD", equity=10000, profit=10000, margin=10000, margin_free=10000, margin_level=10000)
        return account_info

    ####################
    # Order API      #
    ####################
    def order_send(self, request: TradeRequest) -> TradeResult:
        self.socket.send_string("order_send")
        recv_message = self.socket.recv_string()
        print("Receive message = %s" % recv_message)
        result = TradeResult(ticket=123456789, retcode=0)
        return result

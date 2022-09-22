import json
from typing import List
from .type import APIRequest, APIRequestType, Rate, AccountInfo, TradeRequest, TradeResult
import pandas as pd
import zmq
from .utils import to_account_info, to_trade_result, to_rates, to_orders, to_order, to_positions, to_position
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
    # General API      #
    ####################
    def send_config(self, config):
        req = APIRequest(type=APIRequestType.SEND_CONFIG, data=config)
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[send_config] = %s" % recv_message)
        json_data = json.loads(recv_message)
        return json_data

    def stop(self):
        req = APIRequest(type=APIRequestType.STOP, data={})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[stop] = %s" % recv_message)
        json_data = json.loads(recv_message)
        return json_data

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
    # Trade API        #
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

    def get_orders(self):
        req = APIRequest(type=APIRequestType.GET_ORDERS, data={})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_orders] = %s" % recv_message)
        json_data = json.loads(recv_message)
        orders = to_orders(json_data)
        return orders

    def get_order(self, ticket):
        req = APIRequest(type=APIRequestType.GET_ORDER, data={"ticket": ticket})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_order] = %s" % recv_message)
        json_data = json.loads(recv_message)
        order = to_order(json_data)
        return order

    def get_positions(self):
        req = APIRequest(type=APIRequestType.GET_POSITIONS, data={})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_positions] = %s" % recv_message)
        json_data = json.loads(recv_message)
        positions = to_positions(json_data)
        return positions

    def get_position(self, ticket):
        req = APIRequest(type=APIRequestType.GET_POSITION, data={"ticket": ticket})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_position] = %s" % recv_message)
        json_data = json.loads(recv_message)
        position = to_position(json_data)
        return position

    def get_history_orders(self):
        req = APIRequest(type=APIRequestType.GET_HISTORY_ORDERS, data={})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_history_orders] = %s" % recv_message)
        json_data = json.loads(recv_message)
        orders = to_orders(json_data)
        return orders

    def get_history_order(self, ticket):
        req = APIRequest(type=APIRequestType.GET_HISTORY_ORDER, data={"ticket": ticket})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_history_order] = %s" % recv_message)
        json_data = json.loads(recv_message)
        order = to_order(json_data)
        return order

    def get_history_positions(self):
        req = APIRequest(type=APIRequestType.GET_HISTORY_POSITIONS, data={})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_history_positions] = %s" % recv_message)
        json_data = json.loads(recv_message)
        positions = to_positions(json_data)
        return positions

    def get_history_position(self, ticket):
        req = APIRequest(type=APIRequestType.GET_HISTORY_POSITION, data={"ticket": ticket})
        req_str = json.dumps(req._asdict())
        self.socket.send_string(req_str)
        recv_message = self.socket.recv_string()
        logger.debug("[get_history_position] = %s" % recv_message)
        json_data = json.loads(recv_message)
        position = to_position(json_data)
        return position

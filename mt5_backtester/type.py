

from typing import NamedTuple, Union
from enum import Enum

class Order(NamedTuple):
    ticket: int
    type: int
    state: int
    symbol: str
    volume: float
    open_price: float
    stoploss: float
    takeprofit: float
    comment: str
    expiration: int
    reason: int
    timestamp: int

class Position(NamedTuple):
    ticket: int
    symbol: str
    volume: float
    type: int
    open_price: float
    stoploss: float
    takeprofit: float
    swap: float
    profit: float
    comment: str
    timestamp: int

class AccountInfo(NamedTuple):
    balance: float
    credit: float
    currency: str
    equity: float
    profit: float
    margin: float
    margin_free: float
    margin_level: float

class Tick(NamedTuple):
    time: int
    bid: float
    ask: float
    last: float
    volume: float

class Rate(NamedTuple):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    spread: float

class TradeRequest(NamedTuple):
    symbol: str
    type: int
    volume: float
    price: float
    slippage: int
    stoploss: float
    takeprofit: float
    comment: str
    magic: int
    expiration: int

class TradeResult(NamedTuple):
    ticket: int
    retcode: int

class Event(str, Enum):
    ON_TICK = "ON_TICK"
    ON_INIT = "ON_INIT"
    ON_DEINIT = "ON_DEINIT"

class OnTickData(NamedTuple):
    tick: Tick

class StreamData(NamedTuple):
    event: Event
    data: Union[object, OnTickData]

class APIRequestType(str, Enum):
    GET_RATES = "GET_RATES"
    GET_ACCOUNT_INFO = "GET_ACCOUNT_INFO"
    ORDER_SEND = "ORDER_SEND"
    GET_ORDERS = "GET_ORDERS"
    GET_ORDER = "GET_ORDER"
    GET_POSITIONS = "GET_POSITIONS"
    GET_POSITION = "GET_POSITION"
    GET_HISTORY_ORDERS = "GET_HISTORY_ORDERS"
    GET_HISTORY_ORDER = "GET_HISTORY_ORDER"
    GET_HISTORY_POSITIONS = "GET_HISTORY_POSITIONS"
    GET_HISTORY_POSITION = "GET_HISTORY_POSITION"

class APIRequest(NamedTuple):
    type: APIRequestType
    data: object

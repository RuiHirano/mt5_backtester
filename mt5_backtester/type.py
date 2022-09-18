

from typing import NamedTuple, Union
from enum import Enum

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

class TradeTransaction(NamedTuple):
    ticket: int
    order: int
    open_time: int
    open_price: float
    sl: float
    tp: float
    close_time: int
    close_price: float
    commission: float
    swaps: float
    profit: float
    comment: str
    magic: int
    volume: float
    margin_rate: float
    timestamp: int

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

class APIRequest(NamedTuple):
    type: APIRequestType
    data: object

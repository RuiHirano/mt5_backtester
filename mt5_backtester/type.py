

from typing import NamedTuple
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

class StreamData(NamedTuple):
    event: str
    data: object

class Event(Enum):
    ON_TICK = "on_tick"
    ON_INIT = "on_init"
    ON_DEINIT = "on_deinit"

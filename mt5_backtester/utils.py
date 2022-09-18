from typing import Any, Dict, Tuple, List, Union
from .type import StreamData, Event, APIRequest, APIRequestType, TradeResult, AccountInfo, Rate, Tick, OnTickData, Order, Position

def to_tick(tick: Dict) -> Tick:
    return Tick(tick["time"], tick["bid"], tick["ask"], tick["last"], tick["volume"])

def to_stream_data(data: Dict) -> StreamData:
    if Event(data["event"]) == Event.ON_TICK:
        ontick_data = OnTickData(to_tick(data["data"]["tick"]))
        return StreamData(Event(data["event"]), ontick_data)
    return StreamData(Event(data["event"]), data["data"])

def to_api_request(request: Any) -> APIRequest:
    return APIRequest(APIRequestType(request["type"]), request["data"])

def to_trade_result(result: Any) -> TradeResult:
    return TradeResult(result["ticket"], result["retcode"])

def to_account_info(info: Any) -> AccountInfo:
    return AccountInfo(info["balance"], info["credit"], info["currency"], info["equity"], info["profit"], info["margin"], info["margin_free"], info["margin_level"])

def to_rates(rates: List) -> List[Rate]:
    return [Rate(rate["time"], rate["open"], rate["high"], rate["low"], rate["close"], rate["volume"], rate["spread"]) for rate in rates]

def to_order(order: Any) -> Order:
    return Order(order["ticket"], order["symbol"], order["type"], order["state"], order["volume"], order["open_price"], order["stoploss"], order["takeprofit"], order["comment"], order["expiration"], order["timestamp"], order["reason"])

def to_orders(orders: List) -> List[Order]:
    return [to_order(order) for order in orders]

def to_position(position: Any) -> Position:
    return Position(position["ticket"], position["symbol"], position["type"], position["volume"], position["open_price"], position["stoploss"], position["takeprofit"], position["comment"], position["timestamp"], position["swap"], position["profit"])

def to_positions(positions: List) -> List[Position]:
    return [to_position(position) for position in positions]

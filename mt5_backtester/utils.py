from typing import Any, Dict, Tuple, List, Union
from .type import StreamData, Event, APIRequest, APIRequestType, TradeResult, AccountInfo, Rate, Tick, OnTickData

def to_tick(tick: Dict) -> Dict:
    return Tick(tick["time"], tick["bid"], tick["ask"], tick["last"], tick["volume"])

def to_stream_data(data: Dict) -> Tuple:
    if Event(data["event"]) == Event.ON_TICK:
        ontick_data = OnTickData(to_tick(data["data"]["tick"]))
        return StreamData(Event(data["event"]), ontick_data)
    return StreamData(Event(data["event"]), data["data"])

def to_api_request(request: Any) -> Dict:
    return APIRequest(APIRequestType(request["type"]), request["data"])

def to_trade_result(result: Any) -> Dict:
    return TradeResult(result["ticket"], result["retcode"])

def to_account_info(info: Any) -> Dict:
    return AccountInfo(info["balance"], info["credit"], info["currency"], info["equity"], info["profit"], info["margin"], info["margin_free"], info["margin_level"])

def to_rates(rates: List) -> List:
    return [Rate(rate["time"], rate["open"], rate["high"], rate["low"], rate["close"], rate["volume"], rate["spread"]) for rate in rates]

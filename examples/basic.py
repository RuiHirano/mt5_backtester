
from mt5_backtester import Backtester, TradeRequest, Event

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

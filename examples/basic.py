
from mt5_backtester import Backtester, TradeRequest, Event

if __name__ == "__main__":
    with Backtester() as bt:
        for (event, data) in bt.stream():
            if event == Event.ON_INIT:
                print("====== ON_INIT =======")
            elif event == Event.ON_TICK:
                print("====== ON_TICK =======")
                print("tick: ", data.tick)
                rates = bt.api.get_rates("EURUSD", "M1", 0, 0)
                print("rates: ", rates)
                account = bt.api.get_account_info()
                print("account: ", account)
                orders = bt.api.get_orders()
                print("orders: ", orders)
                request = TradeRequest(symbol="EURUSD", volume=0.01, type=0, price=0, stoploss=0, takeprofit=0, magic=0, comment="test", expiration=0, slippage=0)
                result = bt.api.order_send(request)
                print("order send result: ", result)
            elif event == Event.ON_DEINIT:
                print("====== ON_DEINIT =======")

    '''try:
        bt = Backtester()
        for (event, data) in bt.stream():
            if event == Event.ON_INIT:
                print("====== ON_INIT =======")
            elif event == Event.ON_TICK:
                print("====== ON_TICK =======")
                print("tick: ", data.tick)
                rates = bt.api.get_rates("EURUSD", "M1", 0, 0)
                print("rates: ", rates)
                account = bt.api.get_account_info()
                print("account: ", account)
                request = TradeRequest(symbol="EURUSD", volume=0.01, type=0, price=0, stoploss=0, takeprofit=0, magic=0, comment="test", expiration=0, slippage=0)
                result = bt.api.order_send(request)
                print("order send result: ", result)
            elif event == Event.ON_DEINIT:
                print("====== ON_DEINIT =======")
    finally:
        bt.close()'''


if __name__ == "__main__":
    with Backtester() as bt:
        bt.set_config({
            "EA": "TestEA",
            "name": "EURUSD",
        })
        for tick in bt.on_tick():
            print(tick)
            rates = bt.get_rates()
            account_info = bt.get_account_info()
            bt.buy(0.01)

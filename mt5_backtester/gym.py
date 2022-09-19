
from typing import List
from mt5_backtester import Backtester, StreamData, Event, TradeRequest
import gym
import random
import threading

class BacktestEnv(gym.Env):
    def __init__(self):
        self.bt = Backtester()
        self.stream_data = None
        self._setup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _setup(self):
        self.stream_event = threading.Event()
        self.gym_event = threading.Event()
        self.thread = threading.Thread(target=self._stream)
        self.thread.start()

    def _stream(self):
        for (event, data) in self.bt.stream():
            self.stream_data = StreamData(event, data)
            self.gym_event.set()
            self.stream_event.wait()
            self.stream_event.clear()

    def step(self, requests: List[TradeRequest]):
        self.gym_event.wait()
        self.gym_event.clear()
        for request in requests:
            self.bt.api.order_send(request)
        obs = self._observation()
        done = self._done()
        reward = self._reward()
        self.stream_event.set()
        return obs, reward, done, {}

    def reset(self):
        self.gym_event.wait()
        self.gym_event.clear()
        rates = self._observation()
        self.stream_event.set()
        return rates

    def _observation(self):
        return self.bt.api.get_rates("EURUSD", "M1", 0, 0)

    def _done(self):
        if self.stream_data and self.stream_data.event == Event.ON_DEINIT:
            return True
        return False

    def _reward(self):
        if self.stream_data:
            account_info = self.bt.api.get_account_info()
            return account_info.profit
        return 0

    def render(self, mode='human'):
        pass

    def close(self):
        self.bt.close()


if __name__ == "__main__":
    with BacktestEnv() as env:
        for k in range(10): # up to 10 trades
            done = False
            obs = env.reset()
            step = 0
            while not done:
                request = TradeRequest(symbol="EURUSD", volume=0.01, type=0, price=0, stoploss=0, takeprofit=0, magic=0, comment="test", expiration=0, slippage=0)
                next_obs, reward, done, info = env.step([request])
                print("episode: {}, step: {}, done: {}, reward: {}".format(k, step, done, reward))
                step += 1
        print("finished!")
    
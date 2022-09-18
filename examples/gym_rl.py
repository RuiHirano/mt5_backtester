
from mt5_backtester import Backtester, StreamData, Event, AccountInfo
import gym
import random
from enum import Enum
import threading

class Action(Enum):
    BUY = 0
    SELL = 1
    HOLD = 2

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

    def step(self, action: Action):
        self.gym_event.wait()
        self.gym_event.clear()
        rates = self.bt.api.get_rates("EURUSD", "M1", 0, 0)
        done = self._done()
        reward = self._reward()
        self.stream_event.set()
        return rates, reward, done, {}

    def reset(self):
        self.gym_event.wait()
        self.gym_event.clear()
        rates = self.bt.api.get_rates("EURUSD", "M1", 0, 0)
        self.stream_event.set()
        return rates

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
                action = random.choice([a for a in Action])
                next_obs, reward, done, info = env.step(action)
                print("episode: {}, step: {}, done: {}, reward: {}, action: {}".format(k, step, done, reward, action.name))
                step += 1
        print("finished!")
    
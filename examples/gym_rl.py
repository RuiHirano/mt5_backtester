
from mt5_backtester import Event, BacktestEnv, TradeRequest
import random
from enum import Enum

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
        
    '''env = BacktestEnv()
    for k in range(10): # up to 10 trades
        done = False
        obs = env.reset()
        step = 0
        while not done:
            request = TradeRequest(symbol="EURUSD", volume=0.01, type=0, price=0, stoploss=0, takeprofit=0, magic=0, comment="test", expiration=0, slippage=0)
            next_obs, reward, done, info = env.step([request])
            print("episode: {}, step: {}, done: {}, reward: {}".format(k, step, done, reward))
            step += 1
    env.close()
    print("finished!")'''

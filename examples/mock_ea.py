
from mt5_backtester import ExpertAdvisor

if __name__ == "__main__":
    with ExpertAdvisor() as ea:
        ea.run(iter=1000)

import gym
import numpy as np
import logging
from stable_baselines3 import DQN
from stable_baselines3.common.envs import DummyVecEnv
from core.backtester import Backtester
from core.market_data import MarketData
from ml.sentiment_analyzer import SentimentAnalyzer
from core.risk_manager import RiskManager

class RiskAwareTradingEnv(gym.Env):
    """ AI Trading Environment with AI-Driven Risk Management """

    def __init__(self, market_data, backtester, sentiment_analyzer, risk_manager, initial_balance=10000):
        super(RiskAwareTradingEnv, self).__init__()

        self.market_data = market_data
        self.backtester = backtester
        self.sentiment_analyzer = sentiment_analyzer
        self.risk_manager = risk_manager
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.current_step = 0
        self.positions = 0  

        self.action_space = gym.spaces.Discrete(3)  # [0: Hold, 1: Buy, 2: Sell]
        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(7,), dtype=np.float32)

        # Setup logging
        logging.basicConfig(
            filename="logs/drl_trader.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def step(self, action):
        """ Executes simulated trade with AI risk management. """
        obs = self._get_observation()
        reward = 0
        sentiment_score = obs[-2]  
        volatility = obs[-1]  

        position_size = self.risk_manager.calculate_position_size(self.balance, obs[0], sentiment_score)
        stop_loss = self.risk_manager.determine_stop_loss(volatility, sentiment_score)

        if action == 1:  # Buy
            self.positions += 1
            self.balance -= obs[0] * position_size  
            reward = -0.1  

        elif action == 2 and self.positions > 0:  # Sell
            self.positions -= 1
            profit = obs[0] - obs[1]  
            self.balance += obs[0] * position_size  
            reward = profit  

        self.backtester.record_trade(
            symbol="XAUUSD",
            action="buy" if action == 1 else "sell",
            price=obs[0],
            quantity=position_size
        )

        self.current_step += 1
        done = self.current_step >= len(self.market_data)  
        return obs, reward, done, {}

    def reset(self):
        """ Resets paper trading environment for a new test """
        self.current_step = 0
        self.balance = self.initial_balance
        self.positions = 0
        return self._get_observation()

    def _get_observation(self):
        """ Retrieves latest market data, sentiment score, and volatility """
        data = self.market_data.get_live_price("XAUUSD")  
        sentiment = self.sentiment_analyzer.analyze_sentiment()
        sentiment_score = sentiment["Score"]
        volatility = np.random.random()  

        return np.array([
            data,  
            self.balance,  
            self.positions,  
            np.random.random(),  
            np.random.random(),  
            sentiment_score,  
            volatility  
        ])

# Initialize AI Training with Dynamic Risk Management
if __name__ == "__main__":
    market_data = MarketData()
    backtester = Backtester()
    sentiment_analyzer = SentimentAnalyzer()
    risk_manager = RiskManager()

    env = DummyVecEnv([lambda: RiskAwareTradingEnv(market_data, backtester, sentiment_analyzer, risk_manager)])
    model = DQN("MlpPolicy", env, verbose=1)

    print("Training AI Trader with Risk Management...")
    model.learn(total_timesteps=10000)

    print("AI Paper Trader Trained. Running Backtest...")
    backtester.run_backtest()

    print("Paper Trading AI with Risk Management Complete.")
    logging.info("AI Paper Trading Mode with Dynamic Risk Adjustments Active.")

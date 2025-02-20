import logging
import pandas as pd
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.envs import DummyVecEnv
from core.backtester import Backtester
from core.market_data import MarketData
from ml.sentiment_analyzer import SentimentAnalyzer
from core.risk_manager import RiskManager
from core.performance_tracker import PerformanceTracker
from ml.drl_trader import RiskAwareTradingEnv

class AITrainer:
    """ Runs AI Training and Backtesting for Performance Analysis """

    def __init__(self):
        self.market_data = MarketData()
        self.backtester = Backtester()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.risk_manager = RiskManager()
        self.performance_tracker = PerformanceTracker()

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_trainer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def train_ai_trader(self, timesteps=10000):
        """ Trains the AI Trader with Risk Management & Sentiment Analysis """
        env = DummyVecEnv([lambda: RiskAwareTradingEnv(
            self.market_data, self.backtester, self.sentiment_analyzer, self.risk_manager
        )])

        model = DQN("MlpPolicy", env, verbose=1)
        print("🚀 Training AI Trader with Sentiment + Risk Management...")
        model.learn(total_timesteps=timesteps)

        model.save("ml/trained_ai_trader.zip")
        logging.info("AI Training Completed. Model Saved.")

        print("✅ AI Training Complete. Running Backtest...")
        self.backtester.run_backtest()

    def generate_performance_report(self):
        """ Generates AI Trading Performance Report """
        print("\n📊 AI Performance Report 📊")
        metrics = self.performance_tracker.compute_performance_metrics()

        if metrics:
            for key, value in metrics.items():
                print(f"{key}: {value}")

        print("\n✅ AI Performance Report Generated.")

# Run AI Training & Performance Review
if __name__ == "__main__":
    trainer = AITrainer()
    trainer.train_ai_trader()
    trainer.generate_performance_report()

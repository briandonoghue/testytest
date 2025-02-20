import logging
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.envs import DummyVecEnv
from core.backtester import Backtester
from core.market_data import MarketData
from ml.sentiment_analyzer import SentimentAnalyzer
from core.risk_manager import RiskManager
from ml.drl_trader import RiskAwareTradingEnv

class HyperparameterTuner:
    """ Optimizes AI Trader Hyperparameters for Maximum Performance """

    def __init__(self):
        self.market_data = MarketData()
        self.backtester = Backtester()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.risk_manager = RiskManager()

        # Setup logging
        logging.basicConfig(
            filename="logs/hyperparameter_tuner.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def tune_hyperparameters(self):
        """ Runs AI training with different hyperparameters and selects the best one """

        # Hyperparameter Grid
        learning_rates = [0.0001, 0.0005, 0.001]
        batch_sizes = [32, 64, 128]
        discount_factors = [0.95, 0.99]

        best_performance = float("-inf")
        best_params = {}

        for lr in learning_rates:
            for batch in batch_sizes:
                for gamma in discount_factors:
                    print(f"\n🚀 Training AI with LR={lr}, Batch={batch}, Gamma={gamma}")

                    env = DummyVecEnv([lambda: RiskAwareTradingEnv(
                        self.market_data, self.backtester, self.sentiment_analyzer, self.risk_manager
                    )])

                    model = DQN("MlpPolicy", env, verbose=0, learning_rate=lr, batch_size=batch, gamma=gamma)
                    model.learn(total_timesteps=5000)

                    performance = self.backtester.run_backtest()
                    total_profit = performance["Total Profit"]

                    print(f"📈 Profit: {total_profit} | LR={lr}, Batch={batch}, Gamma={gamma}")

                    if total_profit > best_performance:
                        best_performance = total_profit
                        best_params = {"learning_rate": lr, "batch_size": batch, "gamma": gamma}

                    logging.info("Tested AI with LR=%.5f, Batch=%d, Gamma=%.2f -> Profit: %.2f",
                                 lr, batch, gamma, total_profit)

        print("\n✅ Best Hyperparameters Found:", best_params)
        return best_params

# Run AI Hyperparameter Optimization
if __name__ == "__main__":
    tuner = HyperparameterTuner()
    best_params = tuner.tune_hyperparameters()

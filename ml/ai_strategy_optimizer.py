import logging
import pandas as pd
import numpy as np
import multiprocessing
from backtester import Backtester
from strategies.moving_average import MovingAverageStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.volatility_breakout import VolatilityBreakoutStrategy

class AIStrategyOptimizer:
    def __init__(self, market_data, initial_balance=10000):
        """
        Initializes the AI Strategy Optimizer.

        :param market_data: Historical market data (pandas DataFrame).
        :param initial_balance: Starting balance for backtesting.
        """
        self.market_data = market_data
        self.initial_balance = initial_balance

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_strategy_optimizer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def evaluate_strategy(self, strategy_class, params):
        """
        Backtests a trading strategy with given parameters.

        :param strategy_class: Strategy class to test.
        :param params: Dictionary of parameters for strategy tuning.
        :return: Total profit from backtesting.
        """
        strategy = strategy_class(**params)
        backtester = Backtester(strategy, self.market_data, initial_balance=self.initial_balance)
        backtester.run_backtest()
        performance = backtester.calculate_performance(self.initial_balance)
        
        logging.info("Strategy %s tested with params: %s -> Profit: %.2f",
                     strategy_class.__name__, params, performance["Total Profit"])
        return performance["Total Profit"], params

    def optimize_strategies(self):
        """ Optimizes trading strategies using parallel processing. """
        param_grid = [
            {"short_window": 10, "long_window": 50},  # Moving Average
            {"rsi_period": 14, "overbought": 70, "oversold": 30},  # RSI
            {"volatility_period": 20, "breakout_threshold": 1.5}  # Volatility Breakout
        ]

        strategies = [
            (MovingAverageStrategy, param_grid[0]),
            (RSIStrategy, param_grid[1]),
            (VolatilityBreakoutStrategy, param_grid[2])
        ]

        with multiprocessing.Pool(processes=3) as pool:
            results = pool.starmap(self.evaluate_strategy, strategies)

        # Select best strategy
        best_strategy = max(results, key=lambda x: x[0])
        logging.info("Best Strategy: %s with Params: %s -> Profit: %.2f",
                     best_strategy[1], best_strategy[0], best_strategy[0])

        return best_strategy

# Example Usage
if __name__ == "__main__":
    # Mock historical data
    data = pd.DataFrame({
        "Open": [2100, 2105, 2110, 2103, 2098],
        "Close": [2105, 2110, 2103, 2098, 2102]
    })

    optimizer = AIStrategyOptimizer(data)
    best_strategy = optimizer.optimize_strategies()
    print("Best Strategy Selected:", best_strategy)

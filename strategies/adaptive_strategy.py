import logging
import pandas as pd
import numpy as np
from core.market_data import MarketData
from ml.ai_strategy_optimizer import AIStrategyOptimizer

class AdaptiveStrategy:
    """ AI-Generated Adaptive Trading Strategy """

    def __init__(self, config):
        """
        Initializes the adaptive strategy.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.ai_optimizer = AIStrategyOptimizer(config)
        self.strategy_mode = "momentum"  # Default strategy
        self.adaptive_threshold = 0.7  # AI confidence level for switching

        # Setup logging
        logging.basicConfig(
            filename="logs/adaptive_strategy.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def select_strategy(self, market_df):
        """
        Dynamically selects the best strategy based on AI learning.
        :param market_df: Market data DataFrame.
        """
        market_conditions = self.analyze_market_conditions(market_df)

        # Use AI to determine strategy mode
        ai_decision = self.ai_optimizer.generate_trade_signal(market_df)
        confidence_score = ai_decision.get("confidence", 0)

        if confidence_score > self.adaptive_threshold:
            self.strategy_mode = ai_decision.get("strategy", "momentum")

        logging.info(f"Strategy switched to: {self.strategy_mode} with confidence {confidence_score:.2f}")

    def analyze_market_conditions(self, market_df):
        """
        Analyzes market conditions for trend, volatility, and momentum.
        :param market_df: Market data DataFrame.
        :return: Dictionary with market condition indicators.
        """
        if market_df.empty:
            logging.warning("No market data available for analysis.")
            return {}

        market_conditions = {
            "trend": np.sign(market_df["price"].pct_change().sum()),  # Trend direction
            "volatility": market_df["price"].pct_change().std(),  # Volatility measure
            "momentum": market_df["price"].diff().sum(),  # Momentum score
        }

        logging.info(f"Market Conditions: {market_conditions}")
        return market_conditions

    def generate_trade_signal(self, market_df):
        """
        Generates trade signals based on the selected strategy.
        :param market_df: Market data DataFrame.
        :return: Trade signal dictionary.
        """
        self.select_strategy(market_df)

        if self.strategy_mode == "momentum":
            return self.momentum_strategy(market_df)
        elif self.strategy_mode == "mean_reversion":
            return self.mean_reversion_strategy(market_df)
        elif self.strategy_mode == "breakout":
            return self.breakout_strategy(market_df)

        return None

    def momentum_strategy(self, market_df):
        """ Implements a momentum-based trading strategy. """
        last_price = market_df.iloc[-1]["price"]
        sma_50 = market_df["price"].rolling(window=50).mean().iloc[-1]
        if last_price > sma_50:
            return {"symbol": market_df.iloc[-1]["symbol"], "action": "buy", "price": last_price, "quantity": 1}
        return {"symbol": market_df.iloc[-1]["symbol"], "action": "sell", "price": last_price, "quantity": 1}

    def mean_reversion_strategy(self, market_df):
        """ Implements a mean reversion trading strategy. """
        last_price = market_df.iloc[-1]["price"]
        mean_price = market_df["price"].rolling(window=20).mean().iloc[-1]
        if last_price < mean_price:
            return {"symbol": market_df.iloc[-1]["symbol"], "action": "buy", "price": last_price, "quantity": 1}
        return {"symbol": market_df.iloc[-1]["symbol"], "action": "sell", "price": last_price, "quantity": 1}

    def breakout_strategy(self, market_df):
        """ Implements a breakout trading strategy. """
        last_price = market_df.iloc[-1]["price"]
        high_20 = market_df["price"].rolling(window=20).max().iloc[-1]
        if last_price > high_20:
            return {"symbol": market_df.iloc[-1]["symbol"], "action": "buy", "price": last_price, "quantity": 1}
        return None  # No trade signal if no breakout

import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from core.market_data import MarketData
from utilities.error_handler import ErrorHandler

class AIExecutionOptimizer:
    """ AI-driven execution optimizer for trade timing and liquidity tracking """

    def __init__(self, config):
        """
        Initializes the AI execution optimizer.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.error_handler = ErrorHandler()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.liquidity_tracking = config["execution"].get("liquidity_filtering", True)
        self.slippage_tolerance = config["execution"].get("slippage_tolerance", 0.005)

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_execution_optimizer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def analyze_execution_conditions(self, symbol):
        """
        Analyzes market conditions to determine the optimal trade execution window.
        :param symbol: Trading asset symbol.
        :return: Recommended execution timing and order type.
        """
        spread = self.market_data.get_bid_ask_spread(symbol)
        volatility = self.market_data.get_asset_volatility(symbol)
        liquidity_score = self.market_data.get_liquidity_score(symbol)

        if spread is None or volatility is None or liquidity_score is None:
            self.error_handler.log_error(f"Execution analysis failed for {symbol}.", source="AIExecutionOptimizer")
            return None

        # AI-based execution strategy
        execution_delay = np.clip(1 - liquidity_score, 0.1, 2.0)  # Delay execution in low-liquidity environments
        preferred_order_type = "LIMIT" if spread > self.slippage_tolerance else "MARKET"

        logging.info(f"AI Execution Optimization for {symbol}: Delay: {execution_delay:.2f}s, Order Type: {preferred_order_type}")

        return {
            "symbol": symbol,
            "execution_delay": round(execution_delay, 2),
            "preferred_order_type": preferred_order_type
        }

    def optimize_slippage_control(self, trade_signal):
        """
        Adjusts execution logic to reduce slippage.
        :param trade_signal: Trade signal dictionary.
        :return: Adjusted execution parameters.
        """
        symbol = trade_signal["symbol"]
        price = trade_signal["price"]
        liquidity_score = self.market_data.get_liquidity_score(symbol)

        if liquidity_score is None:
            self.error_handler.log_error(f"Slippage control failed for {symbol}.", source="AIExecutionOptimizer")
            return None

        # AI-driven slippage adjustments
        slippage_adjustment = 1 - np.clip(liquidity_score, 0.1, 1.0)  # Lower slippage in high liquidity
        adjusted_price = price * (1 - slippage_adjustment * self.slippage_tolerance)

        logging.info(f"AI Slippage Control for {symbol}: Adjusted Price: {adjusted_price:.2f}, Slippage Factor: {slippage_adjustment:.2f}")

        return {
            "symbol": symbol,
            "adjusted_price": round(adjusted_price, 2)
        }

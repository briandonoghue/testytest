import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from core.market_data import MarketData
from core.performance_tracker import PerformanceTracker
from utilities.error_handler import ErrorHandler

class AIRiskManager:
    """ AI-based risk assessment and trade adjustment system """

    def __init__(self, config):
        """
        Initializes the AI-driven risk management system.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.performance_tracker = PerformanceTracker(config)
        self.error_handler = ErrorHandler()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.max_drawdown = config["risk_management"].get("max_drawdown", 5)
        self.stop_loss_buffer = config["bot_settings"].get("stop_loss_buffer", 0.02)
        self.take_profit_buffer = config["bot_settings"].get("take_profit_buffer", 0.04)

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_risk_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def analyze_trade_risk(self, trade_signal):
        """
        Analyzes trade risk before execution.
        :param trade_signal: Trade signal dictionary.
        :return: Adjusted stop-loss, take-profit, and execution confidence.
        """
        symbol = trade_signal["symbol"]
        action = trade_signal["action"]
        quantity = trade_signal["quantity"]

        # Fetch historical volatility
        volatility = self.market_data.get_asset_volatility(symbol)
        avg_price = self.market_data.get_historical_average(symbol, period="30d")

        if volatility is None or avg_price is None:
            self.error_handler.log_error(f"Risk analysis failed for {symbol}.", source="AIRiskManager")
            return None

        # AI-driven risk calculations
        stop_loss = avg_price * (1 - self.stop_loss_buffer - volatility)
        take_profit = avg_price * (1 + self.take_profit_buffer + volatility)
        execution_confidence = np.clip(1 - volatility, 0.5, 1.0)

        logging.info(f"AI Risk Analysis for {symbol}: Stop Loss: {stop_loss:.2f}, Take Profit: {take_profit:.2f}, Confidence: {execution_confidence:.2f}")

        return {
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "confidence": round(execution_confidence, 2)
        }

    def adjust_risk_levels(self, portfolio_allocation):
        """
        Adjusts portfolio risk exposure based on AI risk predictions.
        :param portfolio_allocation: Dictionary of current asset allocations.
        :return: Adjusted allocations.
        """
        adjusted_allocation = {}
        for asset, allocation in portfolio_allocation.items():
            volatility = self.market_data.get_asset_volatility(asset)
            if volatility is None:
                continue

            # Reduce allocation for high-volatility assets
            risk_factor = 1 - np.clip(volatility, 0.05, 0.2)  # Scale down for volatile assets
            adjusted_allocation[asset] = round(allocation * risk_factor, 2)

        logging.info(f"AI-adjusted Portfolio Risk: {adjusted_allocation}")
        return adjusted_allocation

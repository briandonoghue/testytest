import logging
import numpy as np
from market_data import MarketData
from risk_manager import RiskManager
from datetime import datetime

class AIStopLossOptimizer:
    """AI-driven stop-loss optimization to enhance risk management."""

    def __init__(self, config):
        """
        Initializes the stop-loss optimizer with AI-driven analysis for optimized stop-loss levels.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.risk_manager = RiskManager(config)
        self.stop_loss_factor = config["stop_loss_optimization"]["stop_loss_factor"]
        self.lookback_period = config["stop_loss_optimization"]["lookback_period"]

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_stop_loss_optimizer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def optimize_stop_loss(self, symbol, action, entry_price):
        """
        Optimizes the stop-loss level for a given trade action (buy/sell).
        :param symbol: The asset symbol.
        :param action: The action to be taken, "buy" or "sell".
        :param entry_price: The price at which the asset is bought or sold.
        :return: Optimized stop-loss level.
        """
        # Get historical market data for stop-loss optimization
        market_data = self.market_data.get_historical_data(symbol, period=f"{self.lookback_period}d")
        if market_data is None:
            logging.warning(f"No historical data available for {symbol} to optimize stop-loss.")
            return None

        # Calculate volatility and price movement to determine the optimal stop-loss
        volatility = self.calculate_volatility(market_data)
        price_change = self.calculate_price_change(market_data)
        
        if action == "buy":
            stop_loss = entry_price - (self.stop_loss_factor * volatility)
        elif action == "sell":
            stop_loss = entry_price + (self.stop_loss_factor * volatility)
        else:
            logging.error(f"Invalid action: {action}. Expected 'buy' or 'sell'.")
            return None

        # Ensure stop-loss is within a reasonable range (e.g., no negative stop-loss or extreme levels)
        stop_loss = max(0, stop_loss)  # Prevent negative stop-loss

        logging.info(f"Optimized stop-loss for {symbol} ({action}): {stop_loss:.2f}")
        return stop_loss

    def calculate_volatility(self, market_data):
        """
        Calculates the volatility of an asset based on historical price data.
        :param market_data: DataFrame containing the asset's historical price data.
        :return: Calculated volatility.
        """
        market_data["price_change"] = market_data["price"].pct_change()
        volatility = market_data["price_change"].std()  # Standard deviation of price changes
        return volatility

    def calculate_price_change(self, market_data):
        """
        Calculates the price change over the historical period.
        :param market_data: DataFrame containing the asset's historical price data.
        :return: The overall price change (percent) over the lookback period.
        """
        initial_price = market_data.iloc[0]["price"]
        final_price = market_data.iloc[-1]["price"]
        price_change = (final_price - initial_price) / initial_price
        return price_change

    def adjust_stop_loss_for_market_conditions(self, symbol, action, entry_price):
        """
        Adjusts stop-loss levels based on current market conditions and AI optimization.
        :param symbol: The asset symbol.
        :param action: The action to be taken, "buy" or "sell".
        :param entry_price: The price at which the asset is bought or sold.
        :return: A dictionary with optimized stop-loss and adjustment details.
        """
        stop_loss = self.optimize_stop_loss(symbol, action, entry_price)

        if stop_loss is None:
            return {"status": "Error", "message": f"Stop-loss optimization failed for {symbol}."}

        # Adjust the stop-loss based on further risk management factors
        risk_adjusted_stop_loss = self.risk_manager.adjust_stop_loss(stop_loss, symbol)
        logging.info(f"Risk-adjusted stop-loss for {symbol}: {risk_adjusted_stop_loss:.2f}")
        
        return {"status": "Success", "optimized_stop_loss": risk_adjusted_stop_loss}


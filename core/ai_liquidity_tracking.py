import logging
import numpy as np
from market_data import MarketData
from datetime import datetime

class AILiquidityTracker:
    """AI-driven liquidity tracking to enhance market analysis and risk management."""

    def __init__(self, config):
        """
        Initializes the liquidity tracker with AI techniques for real-time liquidity monitoring.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.liquidity_threshold = config["liquidity_tracking"]["liquidity_threshold"]
        self.lookback_period = config["liquidity_tracking"]["lookback_period"]

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_liquidity_tracker.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def track_liquidity(self, symbol):
        """
        Tracks the liquidity of a market using AI techniques and historical data.
        :param symbol: The asset symbol.
        :return: Liquidity score and market status (High/Low).
        """
        # Fetch historical market data for liquidity tracking
        market_data = self.market_data.get_historical_data(symbol, period=f"{self.lookback_period}d")
        if market_data is None:
            logging.warning(f"No historical data available for {symbol} to track liquidity.")
            return None

        # Calculate liquidity metrics based on trading volume and price movements
        liquidity_score = self.calculate_liquidity(market_data)

        # Classify market liquidity as high or low
        liquidity_status = "High" if liquidity_score >= self.liquidity_threshold else "Low"

        logging.info(f"Liquidity for {symbol}: {liquidity_score:.2f} ({liquidity_status})")
        return liquidity_score, liquidity_status

    def calculate_liquidity(self, market_data):
        """
        Calculates liquidity based on trading volume and price volatility.
        :param market_data: DataFrame containing the asset's historical price and volume data.
        :return: Calculated liquidity score.
        """
        market_data["volume_change"] = market_data["volume"].pct_change()
        market_data["price_change"] = market_data["price"].pct_change()
        
        # Standard deviation of volume changes and price changes
        volume_volatility = market_data["volume_change"].std()
        price_volatility = market_data["price_change"].std()

        # Combine both metrics into a single liquidity score
        liquidity_score = (volume_volatility + price_volatility) / 2  # A simple average of both volatilities
        return liquidity_score

    def adjust_trading_strategy_for_liquidity(self, symbol):
        """
        Adjusts the trading strategy based on the liquidity status of the market.
        :param symbol: The asset symbol.
        :return: Adjusted strategy (e.g., reduce position size in low liquidity).
        """
        liquidity_score, liquidity_status = self.track_liquidity(symbol)

        if liquidity_status == "Low":
            logging.warning(f"Liquidity is low for {symbol}. Adjusting trading strategy.")
            # Reduce position size or avoid trading in low liquidity markets
            adjusted_strategy = self.adjust_for_low_liquidity(symbol)
        else:
            adjusted_strategy = {"status": "Normal", "message": f"Liquidity is high for {symbol}."}

        return adjusted_strategy

    def adjust_for_low_liquidity(self, symbol):
        """
        Reduces position size or adjusts risk management when liquidity is low.
        :param symbol: The asset symbol.
        :return: Adjusted trading strategy.
        """
        # Adjust the risk parameters and trading strategy for low liquidity
        adjusted_risk_factor = self.config["liquidity_tracking"]["low_liquidity_risk_factor"]
        logging.info(f"Reducing risk for {symbol} due to low liquidity.")

        return {
            "status": "Reduced Risk",
            "adjusted_risk_factor": adjusted_risk_factor,
            "message": f"Position size for {symbol} reduced due to low liquidity."
        }

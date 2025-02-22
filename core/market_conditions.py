import logging
import numpy as np
from technical_indicators import TechnicalIndicators
from market_data import MarketData

class MarketConditions:
    """ Class to evaluate and track market conditions using technical indicators and market data """

    def __init__(self, config):
        """
        Initializes the MarketConditions class with configuration and data sources.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.technical_indicators = TechnicalIndicators(config)
        
        # Setup logging
        logging.basicConfig(
            filename="logs/market_conditions.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def evaluate_market_trend(self, symbol):
        """
        Evaluates the current market trend (Bullish, Bearish, Neutral) for a given asset.
        :param symbol: Trading asset symbol.
        :return: Market trend (Bullish, Bearish, Neutral)
        """
        logging.info(f"Evaluating market trend for {symbol}...")

        # Fetch historical market data
        market_data = self.market_data.get_historical_data(symbol, period="60d")
        if market_data is None:
            logging.warning(f"No historical data available for {symbol}.")
            return "Neutral"

        # Calculate technical indicators (e.g., moving averages)
        short_term_ma = self.technical_indicators.calculate_moving_average(symbol, window=20)
        long_term_ma = self.technical_indicators.calculate_moving_average(symbol, window=50)

        # Determine trend based on moving averages
        if short_term_ma > long_term_ma:
            return "Bullish"
        elif short_term_ma < long_term_ma:
            return "Bearish"
        else:
            return "Neutral"

    def check_overbought_oversold(self, symbol):
        """
        Checks if the market is overbought or oversold based on technical indicators like RSI.
        :param symbol: Trading asset symbol.
        :return: Overbought or oversold status
        """
        logging.info(f"Checking overbought/oversold condition for {symbol}...")

        # Fetch historical market data
        market_data = self.market_data.get_historical_data(symbol, period="60d")
        if market_data is None:
            logging.warning(f"No historical data available for {symbol}.")
            return None

        # Calculate RSI (Relative Strength Index)
        rsi = self.technical_indicators.calculate_rsi(symbol, window=14)
        
        if rsi > 70:
            return "Overbought"
        elif rsi < 30:
            return "Oversold"
        else:
            return "Neutral"

    def detect_market_volatility(self, symbol):
        """
        Detects the current market volatility using price standard deviation over the last 20 periods.
        :param symbol: Trading asset symbol.
        :return: Volatility status (High, Low, Normal)
        """
        logging.info(f"Detecting market volatility for {symbol}...")

        # Fetch historical market data
        market_data = self.market_data.get_historical_data(symbol, period="20d")
        if market_data is None:
            logging.warning(f"No historical data available for {symbol}.")
            return "Normal"

        # Calculate price volatility (standard deviation)
        price_volatility = np.std(market_data["price"])

        if price_volatility > 0.02:
            return "High"
        elif price_volatility < 0.01:
            return "Low"
        else:
            return "Normal"

    def evaluate_market_conditions(self, symbol):
        """
        Evaluates the overall market conditions for a given asset using multiple criteria.
        :param symbol: Trading asset symbol.
        :return: Summary of market conditions
        """
        logging.info(f"Evaluating market conditions for {symbol}...")

        trend = self.evaluate_market_trend(symbol)
        overbought_oversold = self.check_overbought_oversold(symbol)
        volatility = self.detect_market_volatility(symbol)

        conditions = {
            "trend": trend,
            "overbought_oversold": overbought_oversold,
            "volatility": volatility
        }

        logging.info(f"Market conditions for {symbol}: {conditions}")
        return conditions

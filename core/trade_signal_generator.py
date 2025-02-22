import logging
import numpy as np
from market_data import MarketData
from technical_indicators import TechnicalIndicators
from sentiment_analysis import SentimentAnalyzer
from ai_trade_confidence import AITradeConfidenceScorer
from ai_trade_explanation import AITradeExplanation
from performance_tracker import PerformanceTracker

class TradeSignalGenerator:
    """
    The TradeSignalGenerator class is responsible for generating trade signals based on
    multiple factors including technical indicators, sentiment analysis, and machine learning-based models.
    """

    def __init__(self, config):
        """
        Initializes the TradeSignalGenerator with configuration settings and dependencies.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.technical_indicators = TechnicalIndicators(config)
        self.sentiment_analyzer = SentimentAnalyzer(config)
        self.ai_trade_confidence = AITradeConfidenceScorer(config)
        self.ai_trade_explanation = AITradeExplanation(config)
        self.performance_tracker = PerformanceTracker(config)

        # Configure logging
        logging.basicConfig(
            filename="logs/trade_signal_generator.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def generate_trade_signal(self, symbol):
        """
        Generates a trade signal (Buy, Sell, Hold) based on various factors such as technical analysis,
        sentiment analysis, and AI-based confidence score.
        :param symbol: Trading asset symbol (e.g., 'AAPL', 'BTC/USD', etc.).
        :return: Trade signal dictionary with action and confidence.
        """
        logging.info(f"Generating trade signal for {symbol}...")

        # Fetch market data (historical data, current price, etc.)
        market_data = self.market_data.get_latest_market_data(symbol)
        if market_data is None:
            logging.error(f"Market data not available for {symbol}.")
            return None

        # Calculate technical indicators (e.g., RSI, MACD, Moving Averages)
        technical_analysis = self.technical_indicators.calculate_technical_indicators(symbol)
        if not technical_analysis:
            logging.error(f"Technical indicators could not be calculated for {symbol}.")
            return None

        # Perform sentiment analysis (if enabled in config)
        sentiment_score = 0
        if self.config["strategy"]["use_sentiment_analysis"]:
            sentiment_score = self.sentiment_analyzer.analyze_sentiment(symbol)
            logging.info(f"Sentiment score for {symbol}: {sentiment_score}")

        # Get AI-based confidence score (AI model-based prediction)
        ai_confidence = self.ai_trade_confidence.predict_trade_confidence(symbol)
        logging.info(f"AI confidence score for {symbol}: {ai_confidence}")

        # Combine all information to create a trade decision
        signal = self._combine_signals(technical_analysis, sentiment_score, ai_confidence)

        # Explain the trade decision
        explanation = self.ai_trade_explanation.explain_trade(signal)
        logging.info(f"Trade explanation for {symbol}: {explanation}")

        # Track performance (optional, can be saved in DB)
        self.performance_tracker.track_signal(symbol, signal)

        return {
            "symbol": symbol,
            "action": signal["action"],
            "confidence_score": ai_confidence,
            "explanation": explanation,
            "technical_analysis": technical_analysis,
            "sentiment_score": sentiment_score
        }

    def _combine_signals(self, technical_analysis, sentiment_score, ai_confidence):
        """
        Combines technical analysis, sentiment score, and AI confidence to make a final trade decision.
        :param technical_analysis: Dictionary with technical analysis data (RSI, MACD, etc.).
        :param sentiment_score: Sentiment score from sentiment analysis.
        :param ai_confidence: AI model-based confidence score.
        :return: Trade signal dictionary with action (Buy, Sell, Hold).
        """
        # Placeholder logic for combining signals (can be refined later with more sophisticated strategies)
        action = "Hold"  # Default action is Hold

        # Buy signal: RSI < 30 (undervalued), sentiment positive, AI confidence high
        if technical_analysis["RSI"] < 30 and sentiment_score > 0.5 and ai_confidence > 0.7:
            action = "Buy"
        
        # Sell signal: RSI > 70 (overvalued), sentiment negative, AI confidence high
        elif technical_analysis["RSI"] > 70 and sentiment_score < -0.5 and ai_confidence > 0.7:
            action = "Sell"
        
        # Neutral signal: If neither condition is met, default to Hold
        else:
            action = "Hold"

        return {
            "action": action,
            "technical_analysis": technical_analysis,
            "sentiment_score": sentiment_score,
            "ai_confidence": ai_confidence
        }

    def generate_trade_signal_batch(self, symbols):
        """
        Generates trade signals for a batch of symbols (assets).
        :param symbols: List of trading symbols (e.g., ['AAPL', 'BTC/USD', 'ETH/USD']).
        :return: List of trade signals for each symbol.
        """
        signals = []
        for symbol in symbols:
            signal = self.generate_trade_signal(symbol)
            if signal:
                signals.append(signal)
        return signals

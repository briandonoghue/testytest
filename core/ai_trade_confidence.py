import logging
import numpy as np
from market_data import MarketData
from sentiment_analysis import SentimentAnalyzer
from technical_indicators import TechnicalIndicators
from market_conditions import MarketConditions

class AITradeConfidenceScorer:
    """ AI-driven trade confidence scoring system """

    def __init__(self, config):
        """
        Initializes the AI Trade Confidence Scorer with various data sources.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.sentiment_analyzer = SentimentAnalyzer(config)
        self.technical_indicators = TechnicalIndicators(config)
        self.market_conditions = MarketConditions(config)
        
        # Setup logging
        logging.basicConfig(
            filename="logs/ai_trade_confidence.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def calculate_confidence_score(self, trade_signal):
        """
        Calculate the confidence score for a trade signal.
        The confidence score is based on various indicators such as technical analysis, sentiment, and market conditions.
        :param trade_signal: Dictionary containing trade signal details.
        :return: A confidence score between 0 and 1.
        """
        symbol = trade_signal["symbol"]
        action = trade_signal["action"]

        # Step 1: Retrieve technical indicators
        technical_score = self._evaluate_technical_indicators(symbol, action)

        # Step 2: Retrieve sentiment analysis score
        sentiment_score = self._evaluate_sentiment(symbol)

        # Step 3: Evaluate market conditions (volatility, trend strength, etc.)
        market_condition_score = self._evaluate_market_conditions(symbol)

        # Step 4: Combine all scores to compute the final confidence score
        total_score = self._combine_scores(technical_score, sentiment_score, market_condition_score)

        # Normalize the score between 0 and 1
        confidence_score = self._normalize_score(total_score)

        logging.info(f"Confidence Score for {symbol} - {action}: {confidence_score:.2f}")
        return confidence_score

    def _evaluate_technical_indicators(self, symbol, action):
        """
        Evaluate technical indicators like RSI, MACD, and moving averages.
        :param symbol: Trading asset symbol.
        :param action: Action to be taken (Buy/Sell/Hold).
        :return: Technical score between 0 and 1.
        """
        rsi = self.technical_indicators.get_rsi(symbol)
        macd = self.technical_indicators.get_macd(symbol)
        moving_avg = self.technical_indicators.get_moving_average(symbol, window=50)

        score = 0
        if action == "Buy":
            if rsi < 30 and macd > 0 and moving_avg > self.market_data.get_latest_price(symbol):
                score = 1.0
            elif rsi < 40 and macd > 0:
                score = 0.75
        elif action == "Sell":
            if rsi > 70 and macd < 0 and moving_avg < self.market_data.get_latest_price(symbol):
                score = 1.0
            elif rsi > 60 and macd < 0:
                score = 0.75
        else:  # Hold
            score = 0.5

        return score

    def _evaluate_sentiment(self, symbol):
        """
        Analyze sentiment based on recent news, social media, or market chatter.
        :param symbol: Trading asset symbol.
        :return: Sentiment score between 0 and 1.
        """
        sentiment = self.sentiment_analyzer.analyze_sentiment(symbol)
        return sentiment

    def _evaluate_market_conditions(self, symbol):
        """
        Analyze broader market conditions, like overall trend and volatility.
        :param symbol: Trading asset symbol.
        :return: Market condition score between 0 and 1.
        """
        trend_strength = self.market_conditions.get_trend_strength(symbol)
        volatility = self.market_conditions.get_volatility(symbol)
        
        # Combine trend strength and volatility to form a market condition score
        score = (trend_strength * 0.7) + (1 - volatility) * 0.3
        return score

    def _combine_scores(self, technical_score, sentiment_score, market_condition_score):
        """
        Combine individual scores into a final confidence score.
        :param technical_score: Technical analysis score.
        :param sentiment_score: Sentiment analysis score.
        :param market_condition_score: Market condition score.
        :return: Combined score.
        """
        # Weight each component (can be adjusted based on strategy preferences)
        weight_technical = 0.4
        weight_sentiment = 0.3
        weight_market_conditions = 0.3

        combined_score = (technical_score * weight_technical +
                          sentiment_score * weight_sentiment +
                          market_condition_score * weight_market_conditions)

        return combined_score

    def _normalize_score(self, score):
        """
        Normalize the score between 0 and 1.
        :param score: Raw combined score.
        :return: Normalized score.
        """
        normalized_score = min(max(score, 0), 1)
        return normalized_score

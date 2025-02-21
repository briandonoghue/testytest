import unittest
import json
from core.ai_trade_confidence import AITradeConfidenceScorer

class TestAITradeConfidenceScore(unittest.TestCase):
    """ Unit tests for AI-powered trade confidence scoring system """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize AITradeConfidenceScorer """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.confidence_scorer = AITradeConfidenceScorer(cls.config)

    def test_confidence_score_calculation(self):
        """ Ensure AI correctly calculates trade confidence scores """
        trade_data = {
            "symbol": "BTCUSDT",
            "technical_indicators": {"RSI": 30, "MACD": "Bullish Crossover"},
            "sentiment_score": 0.5,
            "market_trend": "Uptrend"
        }

        confidence_score = self.confidence_scorer.calculate_confidence_score(trade_data)

        self.assertIsInstance(confidence_score, float, "Confidence score should be a float value")
        self.assertGreaterEqual(confidence_score, 0, "Confidence score should not be negative")
        self.assertLessEqual(confidence_score, 1, "Confidence score should be normalized (0 to 1)")

    def test_low_confidence_trade(self):
        """ Validate AI assigns low confidence to uncertain trades """
        trade_data = {
            "symbol": "ETHUSDT",
            "technical_indicators": {"SMA_50": "Below SMA_200", "Momentum": -0.02},
            "sentiment_score": -0.1,
            "market_trend": "Sideways"
        }

        confidence_score = self.confidence_scorer.calculate_confidence_score(trade_data)

        self.assertLessEqual(confidence_score, 0.5, "AI should assign low confidence to weak trade setups")

    def test_high_confidence_trade(self):
        """ Ensure AI assigns high confidence when multiple factors align """
        trade_data = {
            "symbol": "XAUUSD",
            "technical_indicators": {"RSI": 70, "MACD": "Strong Bullish"},
            "sentiment_score": 0.8,
            "market_trend": "Strong Uptrend"
        }

        confidence_score = self.confidence_scorer.calculate_confidence_score(trade_data)

        self.assertGreaterEqual(confidence_score, 0.8, "AI should assign high confidence when signals align")

    def test_confidence_score_risk_adjustment(self):
        """ Validate AI adjusts confidence scores based on risk exposure """
        trade_data = {
            "symbol": "PL=F",
            "technical_indicators": {"RSI": 60, "Order Flow": "Moderate"},
            "sentiment_score": 0.3,
            "market_trend": "Uptrend",
            "risk_exposure": 0.7
        }

        adjusted_score = self.confidence_scorer.adjust_confidence_for_risk(trade_data)

        self.assertIsInstance(adjusted_score, float, "Adjusted confidence should be a float")
        self.assertLessEqual(adjusted_score, 0.7, "Confidence should be reduced for high-risk trades")

    def test_trade_confidence_log_integration(self):
        """ Ensure AI logs confidence scores for tracking and review """
        confidence_log_entry = {
            "symbol": "BTCUSDT",
            "confidence_score": 0.9,
            "trade_decision": "BUY",
            "timestamp": "2025-02-20 22:00:00"
        }

        log_result = self.confidence_scorer.log_confidence_score(confidence_log_entry)

        self.assertTrue(log_result, "AI should successfully log confidence scores")

if __name__ == "__main__":
    unittest.main()

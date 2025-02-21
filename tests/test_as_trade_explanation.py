import unittest
import json
from core.ai_trade_explanation import AITradeExplanation

class TestAITradeExplanation(unittest.TestCase):
    """ Unit tests for AI-powered trade decision explanations """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize AITradeExplanation """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.trade_explainer = AITradeExplanation(cls.config)

    def test_generate_trade_explanation(self):
        """ Ensure AI provides a structured explanation for trade decisions """
        trade_decision = {
            "symbol": "BTCUSDT",
            "action": "BUY",
            "confidence": 0.85,
            "technical_factors": {"RSI": 35, "MACD": "Bullish Crossover"},
            "sentiment_score": 0.4,
            "market_condition": "Uptrend"
        }

        explanation = self.trade_explainer.generate_explanation(trade_decision)

        self.assertIsInstance(explanation, str, "Trade explanation should be a string")
        self.assertIn("BTCUSDT", explanation, "Explanation should mention the trading symbol")
        self.assertIn("BUY", explanation, "Explanation should mention the trade action")
        self.assertIn("RSI", explanation, "Explanation should reference technical indicators")
        self.assertIn("sentiment", explanation.lower(), "Explanation should include sentiment analysis")

    def test_explanation_with_multiple_factors(self):
        """ Validate AI includes multiple factors in trade explanations """
        trade_decision = {
            "symbol": "ETHUSDT",
            "action": "SELL",
            "confidence": 0.9,
            "technical_factors": {"SMA_50": "Below SMA_200", "Momentum": -0.03},
            "sentiment_score": -0.6,
            "market_condition": "Bearish"
        }

        explanation = self.trade_explainer.generate_explanation(trade_decision)

        self.assertIsInstance(explanation, str, "Explanation should be a string")
        self.assertIn("ETHUSDT", explanation, "Explanation should mention the symbol")
        self.assertIn("SELL", explanation, "Explanation should justify the sell action")
        self.assertIn("Momentum", explanation, "Explanation should include relevant technical factors")

    def test_trade_explanation_logging(self):
        """ Ensure AI logs trade explanations for performance review """
        explanation_log_entry = {
            "symbol": "XAUUSD",
            "trade_action": "BUY",
            "explanation": "The trade was executed due to a bullish RSI divergence and a positive sentiment score."
        }

        log_result = self.trade_explainer.log_trade_explanation(explanation_log_entry)

        self.assertTrue(log_result, "AI should successfully log trade explanations")

    def test_explanation_for_no_trade(self):
        """ Validate AI explains why no trade was taken """
        trade_decision = {
            "symbol": "PL=F",
            "action": "HOLD",
            "confidence": 0.5,
            "technical_factors": {"RSI": 48, "MACD": "Neutral"},
            "sentiment_score": 0.1,
            "market_condition": "Sideways"
        }

        explanation = self.trade_explainer.generate_explanation(trade_decision)

        self.assertIsInstance(explanation, str, "Explanation should be a string")
        self.assertIn("HOLD", explanation, "Explanation should justify why no trade was made")
        self.assertIn("neutral", explanation.lower(), "Explanation should reference market indecision")

if __name__ == "__main__":
    unittest.main()

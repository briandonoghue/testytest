import unittest
import json
from core.ai_trade_risk_adjustment import AITradeRiskAdjustment

class TestAITradeRiskAdjustment(unittest.TestCase):
    """ Unit tests for AI-powered trade risk adjustment system """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize AITradeRiskAdjustment """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.risk_adjustment = AITradeRiskAdjustment(cls.config)

    def test_dynamic_stop_loss_adjustment(self):
        """ Ensure AI correctly adjusts stop-loss levels based on volatility """
        test_trade = {
            "symbol": "BTCUSDT",
            "entry_price": 50000,
            "volatility": 0.06
        }

        adjusted_trade = self.risk_adjustment.adjust_stop_loss(test_trade)

        self.assertIsInstance(adjusted_trade, dict, "Trade data should be returned as a dictionary")
        self.assertGreater(adjusted_trade["stop_loss"], test_trade["entry_price"] * 0.95, "Stop-loss should be adjusted based on volatility")
        self.assertLess(adjusted_trade["stop_loss"], test_trade["entry_price"], "Stop-loss should be below entry price")

    def test_dynamic_take_profit_adjustment(self):
        """ Validate AI optimizes take-profit based on market momentum """
        test_trade = {
            "symbol": "ETHUSDT",
            "entry_price": 3200,
            "momentum": 0.03
        }

        adjusted_trade = self.risk_adjustment.adjust_take_profit(test_trade)

        self.assertIsInstance(adjusted_trade, dict, "Trade data should be returned as a dictionary")
        self.assertGreater(adjusted_trade["take_profit"], test_trade["entry_price"], "Take-profit should be above entry price")
        self.assertLess(adjusted_trade["take_profit"], test_trade["entry_price"] * 1.10, "Take-profit should not be excessively high")

    def test_trade_risk_score_calculation(self):
        """ Ensure AI assigns appropriate risk scores to trades """
        test_trade = {
            "symbol": "XAUUSD",
            "volatility": 0.02,
            "liquidity": 0.8,
            "trend_strength": 0.7
        }

        risk_score = self.risk_adjustment.calculate_trade_risk_score(test_trade)

        self.assertIsInstance(risk_score, float, "Risk score should be a float value")
        self.assertGreaterEqual(risk_score, 0, "Risk score should be non-negative")
        self.assertLessEqual(risk_score, 1, "Risk score should be normalized between 0 and 1")

    def test_trade_size_adjustment(self):
        """ Validate AI adjusts trade size based on risk score """
        test_trade = {
            "symbol": "PL=F",
            "entry_price": 1100,
            "risk_score": 0.75
        }

        adjusted_trade = self.risk_adjustment.adjust_trade_size(test_trade)

        self.assertIsInstance(adjusted_trade, dict, "Adjusted trade data should be a dictionary")
        self.assertGreaterEqual(adjusted_trade["trade_size"], 0.01, "Trade size should be positive")
        self.assertLessEqual(adjusted_trade["trade_size"], 1, "Trade size should not exceed max limit")

    def test_risk_management_log_integration(self):
        """ Ensure AI logs risk adjustments for performance tracking """
        test_trade = {
            "symbol": "BTCUSDT",
            "entry_price": 50500,
            "risk_score": 0.6,
            "stop_loss": 49500,
            "take_profit": 51500
        }

        log_result = self.risk_adjustment.log_risk_adjustments(test_trade)

        self.assertTrue(log_result, "AI should successfully log risk adjustments")

if __name__ == "__main__":
    unittest.main()

import unittest
import json
from core.trade_signal_generator import TradeSignalGenerator

class TestTradeSignalGenerator(unittest.TestCase):
    """ Unit tests for AI-powered trade signal generation """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize TradeSignalGenerator """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.signal_generator = TradeSignalGenerator(cls.config)

    def test_generate_trade_signal(self):
        """ Ensure AI correctly generates a trade signal based on market conditions """
        test_symbol = "BTCUSDT"
        trade_signal = self.signal_generator.generate_signal(test_symbol)

        self.assertIsInstance(trade_signal, dict, "Trade signal should be returned as a dictionary")
        self.assertIn(trade_signal["action"], ["BUY", "SELL", "HOLD"], "Trade signal should be valid")
        self.assertGreaterEqual(trade_signal["confidence"], 0, "Confidence score should be non-negative")
        self.assertLessEqual(trade_signal["confidence"], 1, "Confidence score should be normalized")

    def test_filter_false_signals(self):
        """ Validate AI filters out false or weak trade signals """
        weak_signal = {
            "symbol": "ETHUSDT",
            "action": "BUY",
            "confidence": 0.2
        }

        filtered_signal = self.signal_generator.filter_false_signals(weak_signal)

        self.assertIsNone(filtered_signal, "Weak signals should be filtered out")

    def test_trade_signal_risk_adjustment(self):
        """ Ensure AI adjusts trade signals based on risk analysis """
        trade_signal = {
            "symbol": "XAUUSD",
            "action": "SELL",
            "confidence": 0.85
        }

        adjusted_signal = self.signal_generator.adjust_signal_risk(trade_signal)

        self.assertIsInstance(adjusted_signal, dict, "Adjusted signal should return a dictionary")
        self.assertIn("risk_level", adjusted_signal, "Adjusted signal should include risk level")

    def test_trade_signal_adaptation(self):
        """ Validate AI dynamically adapts signals based on market volatility """
        market_conditions = {
            "volatility": 0.07,
            "liquidity": 0.5,
            "momentum": -0.02
        }

        trade_signal = self.signal_generator.generate_signal("PL=F", market_conditions)

        self.assertIsInstance(trade_signal, dict, "Trade signal should return a dictionary")
        self.assertGreaterEqual(trade_signal["confidence"], 0.5, "AI should avoid weak signals under volatile conditions")

    def test_trade_signal_log_integration(self):
        """ Ensure AI logs generated trade signals for performance analysis """
        test_signal = {
            "symbol": "BTCUSDT",
            "action": "BUY",
            "confidence": 0.8
        }

        log_result = self.signal_generator.log_signal(test_signal)

        self.assertTrue(log_result, "AI should successfully log the trade signal")

if __name__ == "__main__":
    unittest.main()

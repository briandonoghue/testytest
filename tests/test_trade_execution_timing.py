import unittest
import json
from core.trade_execution_timing import TradeExecutionTiming

class TestTradeExecutionTiming(unittest.TestCase):
    """ Unit tests for AI-powered trade execution timing optimization """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize TradeExecutionTiming """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.execution_timing = TradeExecutionTiming(cls.config)

    def test_optimal_trade_timing(self):
        """ Ensure AI identifies the best execution window """
        test_symbol = "BTCUSDT"
        market_conditions = {
            "volatility": 0.03,
            "spread": 0.002,
            "liquidity": 0.85
        }

        optimal_time = self.execution_timing.identify_best_execution_window(test_symbol, market_conditions)

        self.assertIsInstance(optimal_time, dict, "Execution timing should return a dictionary")
        self.assertGreaterEqual(optimal_time["confidence"], 0.7, "AI should only execute in high-confidence windows")
        self.assertIn(optimal_time["preferred_order_type"], ["LIMIT", "MARKET"], "Order type should be valid")

    def test_slippage_control_in_execution(self):
        """ Validate AI minimizes slippage during trade execution """
        test_trade = {"symbol": "ETHUSDT", "price": 3200, "volume": 2}
        execution_data = self.execution_timing.apply_slippage_control(test_trade)

        self.assertIsInstance(execution_data, dict, "Execution data should return a dictionary")
        self.assertGreaterEqual(execution_data["adjusted_price"], 0, "Adjusted price should be non-negative")
        self.assertLessEqual(abs(execution_data["adjusted_price"] - test_trade["price"]), test_trade["price"] * self.execution_timing.slippage_tolerance, "Slippage should be within AI-defined limits")

    def test_trade_execution_speed_adjustment(self):
        """ Ensure AI adjusts trade execution speed dynamically """
        test_symbol = "XAUUSD"
        speed_adjustment = self.execution_timing.adjust_execution_speed(test_symbol, market_volatility=0.06)

        self.assertIsInstance(speed_adjustment, float, "Execution speed adjustment should return a float value")
        self.assertGreaterEqual(speed_adjustment, 0, "Execution delay should be non-negative")
        self.assertLessEqual(speed_adjustment, 5, "Execution delay should be within a reasonable range")

    def test_liquidity_sensitive_trade_execution(self):
        """ Validate AI considers liquidity when executing trades """
        test_symbol = "PL=F"
        execution_result = self.execution_timing.execute_trade_based_on_liquidity(test_symbol, order_size=5)

        self.assertIsInstance(execution_result, dict, "Execution result should return a dictionary")
        self.assertGreaterEqual(execution_result["liquidity_score"], 0.5, "Trade should only execute in moderate to high liquidity conditions")

    def test_execution_log_integration(self):
        """ Ensure AI logs execution timing decisions for analysis """
        test_trade = {
            "symbol": "BTCUSDT",
            "action": "BUY",
            "execution_time": "2025-02-20 19:00:00",
            "execution_price": 50200
        }

        log_result = self.execution_timing.log_execution_timing(test_trade)

        self.assertTrue(log_result, "AI should successfully log execution timing decisions")

if __name__ == "__main__":
    unittest.main()

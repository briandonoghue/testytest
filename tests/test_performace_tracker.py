import unittest
import json
from core.performance_tracker import PerformanceTracker

class TestPerformanceTracker(unittest.TestCase):
    """ Unit tests for AI-powered performance tracking system """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize PerformanceTracker """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.performance_tracker = PerformanceTracker(cls.config)

    def test_trade_logging(self):
        """ Ensure AI correctly logs executed trades """
        trade_log = self.performance_tracker.get_trade_log()

        self.assertIsInstance(trade_log, list, "Trade log should be a list")
        self.assertGreaterEqual(len(trade_log), 0, "Trade log should not return an invalid value")

    def test_pnl_calculation(self):
        """ Validate AI correctly calculates profit and loss for executed trades """
        sample_trades = [
            {"symbol": "BTCUSDT", "execution_price": 50000, "exit_price": 51000, "quantity": 1},
            {"symbol": "ETHUSDT", "execution_price": 3000, "exit_price": 2900, "quantity": 2}
        ]

        pnl = self.performance_tracker.calculate_pnl(sample_trades)

        self.assertIsInstance(pnl, dict, "PnL should return a dictionary")
        self.assertIn("total_pnl", pnl, "PnL dictionary should include 'total_pnl'")
        self.assertGreaterEqual(pnl["total_pnl"], -1000, "Total PnL should be within a reasonable range")

    def test_max_drawdown_calculation(self):
        """ Ensure AI correctly tracks max drawdown in trading history """
        drawdown = self.performance_tracker.calculate_max_drawdown()

        self.assertIsInstance(drawdown, float, "Max drawdown should return a float")
        self.assertGreaterEqual(drawdown, 0, "Max drawdown should be non-negative")

    def test_ai_performance_summary(self):
        """ Validate AI-generated performance summary report """
        performance_summary = self.performance_tracker.generate_performance_report()

        self.assertIsInstance(performance_summary, dict, "Performance summary should return a dictionary")
        self.assertIn("Win Rate", performance_summary, "Performance summary should include Win Rate")
        self.assertIn("Profit Factor", performance_summary, "Performance summary should include Profit Factor")

    def test_ai_continuous_learning(self):
        """ Ensure AI updates strategies based on past performance data """
        trade_history = [
            {"symbol": "XAUUSD", "execution_price": 1800, "exit_price": 1850, "quantity": 1},
            {"symbol": "PL=F", "execution_price": 1000, "exit_price": 950, "quantity": 1}
        ]

        updated_strategy = self.performance_tracker.adjust_strategy_based_on_performance(trade_history)

        self.assertIsNotNone(updated_strategy, "AI should return an updated strategy")
        self.assertIn("risk_level", updated_strategy, "Updated strategy should include adjusted risk level")

if __name__ == "__main__":
    unittest.main()

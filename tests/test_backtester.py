import unittest
import json
from core.backtester import Backtester

class TestBacktester(unittest.TestCase):
    """ Unit tests for AI-powered backtesting system """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize Backtester """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.backtester = Backtester(cls.config)

    def test_backtest_trade_execution(self):
        """ Ensure AI executes backtest trades correctly using historical data """
        test_asset = "BTCUSDT"
        backtest_result = self.backtester.run_backtest(test_asset, period="180d")

        self.assertIsInstance(backtest_result, dict, "Backtest result should return a dictionary")
        self.assertIn("total_pnl", backtest_result, "Backtest result should contain 'total_pnl'")
        self.assertIn("win_rate", backtest_result, "Backtest result should contain 'win_rate'")

    def test_backtest_profitability(self):
        """ Validate AI calculates backtest profitability correctly """
        test_asset = "ETHUSDT"
        backtest_result = self.backtester.run_backtest(test_asset, period="90d")

        self.assertGreaterEqual(backtest_result["total_pnl"], -1000, "Backtest total profit should not be extremely negative")
        self.assertGreaterEqual(backtest_result["win_rate"], 0, "Win rate should not be negative")

    def test_ai_historical_trade_accuracy(self):
        """ Ensure AI trades in backtests closely match historical patterns """
        test_asset = "XAUUSD"
        historical_performance = self.backtester.validate_historical_trade_accuracy(test_asset, period="120d")

        self.assertIsInstance(historical_performance, dict, "Historical trade accuracy should return a dictionary")
        self.assertIn("accuracy", historical_performance, "Trade accuracy should include 'accuracy'")
        self.assertGreaterEqual(historical_performance["accuracy"], 60, "AI backtest accuracy should be at least 60%")

    def test_risk_adjustment_during_backtest(self):
        """ Validate AI correctly adjusts risk settings in backtests """
        test_asset = "PL=F"
        backtest_result = self.backtester.run_backtest(test_asset, period="60d")

        self.assertIn("risk_level", backtest_result, "Backtest should include AI-adjusted risk levels")
        self.assertGreaterEqual(backtest_result["risk_level"], 0, "Risk level should be non-negative")

    def test_backtest_report_generation(self):
        """ Ensure AI generates a detailed backtest report after simulation """
        test_asset = "BTCUSDT"
        report = self.backtester.generate_backtest_report(test_asset)

        self.assertIsInstance(report, dict, "Backtest report should return a dictionary")
        self.assertIn("performance_summary", report, "Backtest report should include performance summary")
        self.assertGreaterEqual(len(report["trade_details"]), 5, "Backtest report should include multiple trades for analysis")

if __name__ == "__main__":
    unittest.main()

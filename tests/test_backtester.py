import unittest
import pandas as pd
from core.backtester import Backtester
from config.config import load_config

class TestBacktester(unittest.TestCase):
    """Unit tests for the Backtester module"""

    @classmethod
    def setUpClass(cls):
        """Initialize test dependencies before running tests"""
        config = load_config()
        cls.backtester = Backtester()
        cls.test_symbol = "GC=F"  # Gold futures for testing

        # Sample historical data for backtesting
        cls.sample_data = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "Open": [1800, 1820, 1840, 1860, 1880],
            "High": [1820, 1840, 1860, 1880, 1900],
            "Low": [1790, 1810, 1830, 1850, 1870],
            "Close": [1810, 1830, 1850, 1870, 1890],
            "Volume": [1000, 1200, 1400, 1600, 1800]
        })
        cls.sample_data.set_index("Date", inplace=True)

    def test_backtest_execution(self):
        """Test running a backtest on historical data"""
        print("\n🔍 Running test: Backtest Execution")
        results = self.backtester.run_backtest(
            asset_symbol=self.test_symbol,
            historical_data=self.sample_data,
            strategy_name="SMA_Crossover"
        )
        self.assertIsInstance(results, dict, "❌ Backtest did not return expected dictionary.")
        self.assertIn("final_balance", results, "❌ Missing final balance in backtest results.")

    def test_performance_metrics(self):
        """Test calculating performance metrics"""
        print("\n🔍 Running test: Performance Metrics Calculation")
        performance = self.backtester.calculate_performance_metrics(
            initial_balance=10000,
            trade_history=[
                {"trade_type": "BUY", "price": 1800, "quantity": 1},
                {"trade_type": "SELL", "price": 1850, "quantity": 1}
            ]
        )
        self.assertIsInstance(performance, dict, "❌ Performance metrics should return a dictionary.")
        self.assertIn("profit_loss", performance, "❌ Profit/Loss missing in results.")
        self.assertGreaterEqual(performance["profit_loss"], 0, "❌ Profit/Loss calculation incorrect.")

    def test_risk_adjusted_return(self):
        """Test calculating Sharpe ratio and other risk-adjusted returns"""
        print("\n🔍 Running test: Risk-Adjusted Returns")
        sharpe_ratio = self.backtester.calculate_sharpe_ratio(
            returns=[0.01, 0.02, -0.01, 0.03, -0.02]
        )
        self.assertIsInstance(sharpe_ratio, float, "❌ Sharpe Ratio should be a float.")
        self.assertGreater(sharpe_ratio, -5, "❌ Sharpe Ratio is unrealistic.")

    def test_invalid_strategy(self):
        """Test handling of invalid strategy names"""
        print("\n🔍 Running test: Invalid Strategy Handling")
        results = self.backtester.run_backtest(
            asset_symbol=self.test_symbol,
            historical_data=self.sample_data,
            strategy_name="INVALID_STRATEGY"
        )
        self.assertIsNone(results, "❌ Invalid strategy should return None.")

    def test_trade_logging(self):
        """Test if backtesting trades are logged correctly"""
        print("\n🔍 Running test: Backtest Trade Logging")
        trade = {
            "trade_type": "BUY",
            "price": 1810,
            "quantity": 1,
            "timestamp": "2023-01-01 12:00:00"
        }
        self.backtester.log_trade(trade)
        with open("logs/backtest_logs.txt", "r") as log_file:
            logs = log_file.readlines()
        self.assertTrue(any(str(trade["timestamp"]) in log for log in logs), "❌ Trade log missing.")

if __name__ == "__main__":
    unittest.main()

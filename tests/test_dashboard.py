import unittest
import os
import pandas as pd
from dashboard.dashboard import Dashboard
from core.performance_tracker import PerformanceTracker
from config.config import load_config

class TestDashboard(unittest.TestCase):
    """Unit tests for the Dashboard module"""

    @classmethod
    def setUpClass(cls):
        """Initialize test dependencies before running tests"""
        cls.config = load_config()
        cls.dashboard = Dashboard()
        cls.performance_tracker = PerformanceTracker()

        # Create sample performance data for testing
        cls.sample_performance_data = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
            "Balance": [10000, 10100, 10250, 9900, 10500],
            "Win Rate": [50, 55, 57, 53, 60],
            "Sharpe Ratio": [1.2, 1.3, 1.5, 1.1, 1.7],
            "Max Drawdown": [-5.0, -4.8, -4.6, -6.0, -4.0]
        })
        cls.sample_performance_data.set_index("Date", inplace=True)

    def test_dashboard_initialization(self):
        """Test that the dashboard initializes properly"""
        print("\n🔍 Running test: Dashboard Initialization")
        self.assertIsNotNone(self.dashboard, "❌ Dashboard instance failed to initialize.")

    def test_load_performance_metrics(self):
        """Test loading performance metrics into the dashboard"""
        print("\n🔍 Running test: Load Performance Metrics")
        metrics = self.performance_tracker.get_performance_metrics()
        self.assertIsInstance(metrics, dict, "❌ Performance metrics should be a dictionary.")
        self.assertIn("balance", metrics, "❌ Balance missing in performance metrics.")
        self.assertIn("win_rate", metrics, "❌ Win rate missing in performance metrics.")

    def test_display_dashboard(self):
        """Test the display function of the dashboard"""
        print("\n🔍 Running test: Dashboard Display")
        try:
            self.dashboard.display_dashboard(self.sample_performance_data)
        except Exception as e:
            self.fail(f"❌ Dashboard display failed with error: {e}")

    def test_export_performance_report(self):
        """Test exporting performance reports to a CSV file"""
        print("\n🔍 Running test: Export Performance Report")
        export_path = "logs/performance_report.csv"
        self.dashboard.export_performance_report(self.sample_performance_data, export_path)
        self.assertTrue(os.path.exists(export_path), "❌ Performance report not saved correctly.")

    def test_error_logging(self):
        """Test if dashboard logs errors correctly"""
        print("\n🔍 Running test: Error Logging")
        error_message = "Test Error in Dashboard"
        self.dashboard.log_error(error_message)
        
        with open("logs/error_logs.txt", "r") as log_file:
            logs = log_file.readlines()
        
        self.assertTrue(any(error_message in log for log in logs), "❌ Error log missing.")

    def test_real_time_updates(self):
        """Test if real-time updates function properly"""
        print("\n🔍 Running test: Real-Time Updates")
        try:
            self.dashboard.update_real_time_metrics({
                "balance": 10500,
                "win_rate": 60,
                "sharpe_ratio": 1.7,
                "max_drawdown": -4.0
            })
        except Exception as e:
            self.fail(f"❌ Real-time update failed with error: {e}")

if __name__ == "__main__":
    unittest.main()

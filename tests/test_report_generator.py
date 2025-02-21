import unittest
import os
from utilities.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    """ Unit tests for AI-powered trade report generation """

    @classmethod
    def setUpClass(cls):
        """ Initialize ReportGenerator and define test output path """
        cls.report_generator = ReportGenerator()
        cls.test_report_path = "reports/test_trade_report.pdf"

    def test_generate_daily_report(self):
        """ Ensure AI correctly generates a daily trade report """
        test_data = {
            "total_trades": 10,
            "win_rate": 75.0,
            "total_profit": 1500.0,
            "max_drawdown": 5.2,
            "sharpe_ratio": 1.8
        }

        result = self.report_generator.generate_daily_report(test_data, self.test_report_path)

        self.assertTrue(result, "Daily report should be successfully generated")
        self.assertTrue(os.path.exists(self.test_report_path), "Generated report file should exist")

    def test_generate_weekly_summary(self):
        """ Validate AI generates a weekly trading summary """
        test_data = {
            "weekly_pnl": 4500.0,
            "top_performing_assets": ["BTCUSDT", "XAUUSD"],
            "average_trade_duration": "5h 30m",
            "total_trades": 50,
            "profit_factor": 2.3
        }

        result = self.report_generator.generate_weekly_summary(test_data, self.test_report_path)

        self.assertTrue(result, "Weekly summary should be successfully generated")
        self.assertTrue(os.path.exists(self.test_report_path), "Generated weekly report file should exist")

    def test_generate_monthly_report(self):
        """ Ensure AI creates a full monthly performance report """
        test_data = {
            "monthly_pnl": 18500.0,
            "best_strategy": "Momentum Trading",
            "worst_strategy": "Mean Reversion",
            "risk_adjustments_made": 5,
            "trade_success_rate": 68.5
        }

        result = self.report_generator.generate_monthly_report(test_data, self.test_report_path)

        self.assertTrue(result, "Monthly report should be successfully generated")
        self.assertTrue(os.path.exists(self.test_report_path), "Generated monthly report file should exist")

    def test_report_data_format_validation(self):
        """ Validate AI report generation fails for incorrect data formats """
        invalid_data = "This is not a dictionary"

        result = self.report_generator.generate_daily_report(invalid_data, self.test_report_path)

        self.assertFalse(result, "AI should not generate reports with invalid data")

    def test_report_cleanup(self):
        """ Ensure AI cleans up old reports after a retention period """
        cleanup_result = self.report_generator.cleanup_old_reports("reports/", max_reports=5)

        self.assertTrue(cleanup_result, "Report cleanup should execute successfully")

if __name__ == "__main__":
    unittest.main()

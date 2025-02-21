import unittest
import json
from flask import Flask
from dashboard.api import create_dashboard_api

class TestDashboardAPI(unittest.TestCase):
    """ Unit tests for AI-powered dashboard API endpoints """

    @classmethod
    def setUpClass(cls):
        """ Initialize Flask test client for the dashboard API """
        app = Flask(__name__)
        app = create_dashboard_api(app)
        cls.client = app.test_client()

    def test_get_trade_history(self):
        """ Ensure AI dashboard provides valid trade history """
        response = self.client.get("/api/trade_history")

        self.assertEqual(response.status_code, 200, "API should return a successful response")
        trade_data = json.loads(response.data)

        self.assertIsInstance(trade_data, list, "Trade history should return a list")
        if trade_data:
            self.assertIn("symbol", trade_data[0], "Trade data should include 'symbol'")
            self.assertIn("action", trade_data[0], "Trade data should include 'action'")

    def test_get_risk_metrics(self):
        """ Validate AI dashboard provides real-time risk metrics """
        response = self.client.get("/api/risk_metrics")

        self.assertEqual(response.status_code, 200, "API should return a successful response")
        risk_data = json.loads(response.data)

        self.assertIsInstance(risk_data, dict, "Risk metrics should return a dictionary")
        self.assertIn("max_drawdown", risk_data, "Risk metrics should include 'max_drawdown'")
        self.assertGreaterEqual(risk_data["max_drawdown"], 0, "Max drawdown should be non-negative")

    def test_get_performance_summary(self):
        """ Ensure AI dashboard provides accurate performance summary """
        response = self.client.get("/api/performance_summary")

        self.assertEqual(response.status_code, 200, "API should return a successful response")
        performance_data = json.loads(response.data)

        self.assertIsInstance(performance_data, dict, "Performance summary should return a dictionary")
        self.assertIn("win_rate", performance_data, "Performance summary should include 'win_rate'")
        self.assertGreaterEqual(performance_data["win_rate"], 0, "Win rate should be valid")

    def test_api_error_handling(self):
        """ Validate AI dashboard API handles failures gracefully """
        response = self.client.get("/api/invalid_endpoint")

        self.assertEqual(response.status_code, 404, "API should return 404 for invalid endpoints")

if __name__ == "__main__":
    unittest.main()

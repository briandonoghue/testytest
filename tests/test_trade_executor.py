import unittest
from unittest.mock import patch
from core.trade_executor import TradeExecutor
from core.risk_manager import RiskManager

class TestTradeExecutor(unittest.TestCase):
    def setUp(self):
        """ Initializes TradeExecutor with a mock API. """
        self.mock_api = "https://mock-broker.com/orders"
        self.risk_manager = RiskManager()
        self.trade_executor = TradeExecutor(self.mock_api, self.risk_manager)

    @patch("core.trade_executor.requests.post")
    def test_execute_valid_trade(self, mock_post):
        """ Tests successful trade execution. """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "filled", "order_id": "12345"}

        trade = {"symbol": "XAUUSD", "quantity": 1, "price": 2100.00, "type": "buy"}
        result = self.trade_executor.execute_trade(trade)

        self.assertEqual(result["status"], "filled")
        self.assertIn("order_id", result)

    @patch("core.trade_executor.requests.post")
    def test_execute_invalid_trade(self, mock_post):
        """ Tests rejection of invalid trades. """
        trade = {"symbol": "XAUUSD", "quantity": -1, "price": 2100.00, "type": "buy"}
        result = self.trade_executor.execute_trade(trade)

        self.assertEqual(result["status"], "failed")

    @patch("core.trade_executor.requests.post")
    def test_api_failure_handling(self, mock_post):
        """ Tests API failure & error handling. """
        mock_post.side_effect = Exception("Broker API down")

        trade = {"symbol": "XAUUSD", "quantity": 1, "price": 2100.00, "type": "buy"}
        result = self.trade_executor.execute_trade(trade)

        self.assertEqual(result["status"], "failed")
        self.assertIn("reason", result)

if __name__ == "__main__":
    unittest.main()

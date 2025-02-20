import unittest
from unittest.mock import patch, MagicMock
from core.order_manager import OrderManager

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        """ Initializes OrderManager with a mock broker API. """
        self.mock_api = "https://mock-broker.com/orders"
        self.order_manager = OrderManager(self.mock_api)

    @patch("core.order_manager.requests.post")
    def test_execute_valid_order(self, mock_post):
        """ Tests successful order execution. """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "filled", "order_id": "12345"}

        order = {"symbol": "XAUUSD", "quantity": 1, "price": 2100.00, "type": "limit"}
        result = self.order_manager.execute_order(order)

        self.assertEqual(result["status"], "filled")
        self.assertIn("order_id", result)

    @patch("core.order_manager.requests.post")
    def test_execute_invalid_order(self, mock_post):
        """ Tests rejection of invalid orders. """
        order = {"symbol": "XAUUSD", "quantity": -1, "price": 2100.00, "type": "limit"}
        result = self.order_manager.execute_order(order)

        self.assertEqual(result["status"], "failed")

    @patch("core.order_manager.requests.post")
    def test_api_failure_handling(self, mock_post):
        """ Tests API failure & proper error handling. """
        mock_post.side_effect = Exception("Broker API down")

        order = {"symbol": "XAUUSD", "quantity": 1, "price": 2100.00, "type": "limit"}
        result = self.order_manager.execute_order(order)

        self.assertEqual(result["status"], "failed")
        self.assertIn("reason", result)

if __name__ == "__main__":
    unittest.main()

import unittest
import os
import json
from utilities.trade_logger import TradeLogger

class TestTradeLogger(unittest.TestCase):
    """ Unit tests for AI-powered trade logging system """

    @classmethod
    def setUpClass(cls):
        """ Initialize TradeLogger and set up test log file """
        cls.trade_logger = TradeLogger()
        cls.test_log_file = cls.trade_logger.trade_log_file

        # Ensure test log file is reset
        if os.path.exists(cls.test_log_file):
            os.remove(cls.test_log_file)

    def test_log_trade_execution(self):
        """ Ensure AI logs executed trades correctly """
        test_trade = {
            "symbol": "BTCUSDT",
            "action": "BUY",
            "quantity": 1,
            "execution_price": 50000,
            "timestamp": "2025-02-20 18:30:00"
        }

        log_result = self.trade_logger.log_trade(test_trade)

        self.assertTrue(log_result, "Trade should be successfully logged")

        # Verify log file was created
        self.assertTrue(os.path.exists(self.test_log_file), "Trade log file should be created")

        # Verify trade execution log was recorded
        with open(self.test_log_file, "r") as f:
            logs = json.load(f)

        self.assertGreater(len(logs), 0, "Trade log should not be empty")
        self.assertEqual(logs[-1]["symbol"], "BTCUSDT", "Logged trade should match the executed trade")
        self.assertEqual(logs[-1]["action"], "BUY", "Trade action should match")

    def test_trade_log_retrieval(self):
        """ Validate AI retrieves logged trade history correctly """
        trade_history = self.trade_logger.get_trade_history(limit=3)

        self.assertIsInstance(trade_history, list, "Trade history should return a list")
        self.assertLessEqual(len(trade_history), 3, "Returned trade logs should not exceed requested limit")

    def test_duplicate_trade_entries(self):
        """ Ensure AI prevents duplicate trade entries in logs """
        test_trade = {
            "symbol": "ETHUSDT",
            "action": "SELL",
            "quantity": 2,
            "execution_price": 3000,
            "timestamp": "2025-02-20 18:35:00"
        }

        first_log = self.trade_logger.log_trade(test_trade)
        second_log = self.trade_logger.log_trade(test_trade)

        self.assertTrue(first_log, "First trade should be logged successfully")
        self.assertFalse(second_log, "Duplicate trade should not be logged")

    def test_trade_log_retention_policy(self):
        """ Ensure AI enforces log retention policy for storage management """
        self.trade_logger.log_trade({"symbol": "XAUUSD", "action": "BUY", "quantity": 5, "execution_price": 1850})
        self.trade_logger.enforce_log_retention(max_entries=5)

        with open(self.test_log_file, "r") as f:
            logs = json.load(f)

        self.assertLessEqual(len(logs), 5, "Log retention should enforce a maximum number of entries")

if __name__ == "__main__":
    unittest.main()

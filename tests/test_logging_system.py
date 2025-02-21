import unittest
import os
import json
from utilities.logging_system import LoggingSystem

class TestLoggingSystem(unittest.TestCase):
    """ Unit tests for AI-driven system-wide logging """

    @classmethod
    def setUpClass(cls):
        """ Initialize LoggingSystem and setup test logs """
        cls.logging_system = LoggingSystem()
        cls.test_log_file = cls.logging_system.log_file

        # Ensure test log file is reset
        if os.path.exists(cls.test_log_file):
            os.remove(cls.test_log_file)

    def test_log_trade_execution(self):
        """ Ensure AI logs trade execution details correctly """
        test_trade = {
            "symbol": "BTCUSDT",
            "action": "BUY",
            "quantity": 1,
            "execution_price": 50000,
            "timestamp": "2025-02-20 18:00:00"
        }

        self.logging_system.log_trade_execution(test_trade)

        # Verify log file was created
        self.assertTrue(os.path.exists(self.test_log_file), "Trade log file should be created")

        # Verify trade execution log was recorded
        with open(self.test_log_file, "r") as f:
            logs = json.load(f)

        self.assertGreater(len(logs), 0, "Trade log should not be empty")
        self.assertEqual(logs[-1]["symbol"], "BTCUSDT", "Logged symbol should match trade")
        self.assertEqual(logs[-1]["action"], "BUY", "Logged action should match trade")

    def test_log_system_health(self):
        """ Validate AI logs system health metrics correctly """
        test_health_metrics = {
            "cpu_usage": 30.5,
            "memory_usage": 45.2,
            "disk_space": 120.0
        }

        self.logging_system.log_system_health(test_health_metrics)

        with open(self.test_log_file, "r") as f:
            logs = json.load(f)

        self.assertGreater(len(logs), 1, "System health log should be recorded")
        self.assertIn("cpu_usage", logs[-1], "System health log should include CPU usage")
        self.assertGreaterEqual(logs[-1]["memory_usage"], 0, "Memory usage should be non-negative")

    def test_log_retention_policy(self):
        """ Ensure AI logs are automatically pruned when exceeding retention limits """
        self.logging_system.log_trade_execution({"symbol": "ETHUSDT", "action": "SELL", "quantity": 2, "execution_price": 3000})

        self.logging_system.enforce_log_retention(max_entries=2)

        with open(self.test_log_file, "r") as f:
            logs = json.load(f)

        self.assertLessEqual(len(logs), 2, "Log retention policy should enforce a maximum number of entries")

    def test_fetch_recent_logs(self):
        """ Validate AI can retrieve recent logs for debugging """
        recent_logs = self.logging_system.get_recent_logs(limit=3)

        self.assertIsInstance(recent_logs, list, "Recent logs should return a list")
        self.assertLessEqual(len(recent_logs), 3, "Returned logs should not exceed the requested limit")

if __name__ == "__main__":
    unittest.main()

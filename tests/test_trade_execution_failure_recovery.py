import unittest
import json
from core.trade_execution_failure_recovery import TradeExecutionFailureRecovery

class TestTradeExecutionFailureRecovery(unittest.TestCase):
    """ Unit tests for AI-powered trade execution failure recovery """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize TradeExecutionFailureRecovery """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.execution_recovery = TradeExecutionFailureRecovery(cls.config)

    def test_detect_trade_execution_failure(self):
        """ Ensure AI correctly detects failed trades """
        failed_trade = {
            "symbol": "BTCUSDT",
            "order_id": "12345",
            "status": "FAILED"
        }

        failure_detected = self.execution_recovery.detect_trade_failure(failed_trade)

        self.assertTrue(failure_detected, "AI should correctly detect a failed trade execution")

    def test_trade_retry_mechanism(self):
        """ Validate AI retries failed trades intelligently """
        failed_trade = {
            "symbol": "ETHUSDT",
            "order_id": "67890",
            "status": "FAILED",
            "execution_type": "MARKET"
        }

        retry_result = self.execution_recovery.retry_failed_trade(failed_trade)

        self.assertIsInstance(retry_result, dict, "Trade retry should return a dictionary")
        self.assertIn(retry_result["status"], ["SUCCESS", "FAILED"], "Retry status should be valid")
        self.assertNotEqual(retry_result["order_id"], failed_trade["order_id"], "Retried order should have a new ID")

    def test_execution_strategy_switching(self):
        """ Ensure AI switches execution strategies when failures occur """
        trade_data = {
            "symbol": "XAUUSD",
            "initial_order_type": "LIMIT",
            "order_status": "FAILED"
        }

        switched_order = self.execution_recovery.switch_execution_strategy(trade_data)

        self.assertIsInstance(switched_order, dict, "Strategy-switched order should be a dictionary")
        self.assertNotEqual(switched_order["order_type"], trade_data["initial_order_type"], "AI should switch order type if needed")

    def test_trade_failure_log_integration(self):
        """ Ensure AI logs failed trade executions for analysis """
        failed_trade_log = {
            "symbol": "PL=F",
            "order_id": "00001",
            "failure_reason": "Insufficient Liquidity",
            "timestamp": "2025-02-20 21:00:00"
        }

        log_result = self.execution_recovery.log_trade_failure(failed_trade_log)

        self.assertTrue(log_result, "AI should successfully log trade execution failures")

if __name__ == "__main__":
    unittest.main()

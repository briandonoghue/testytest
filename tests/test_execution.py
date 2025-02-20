import unittest
from core.trade_executor import TradeExecutor
from core.order_manager import OrderManager
from core.risk_manager import RiskManager
from config.config import load_config

class TestTradeExecution(unittest.TestCase):
    """Unit tests for the TradeExecutor module"""

    @classmethod
    def setUpClass(cls):
        """Initialize test dependencies before running tests"""
        config = load_config()
        cls.trade_executor = TradeExecutor()
        cls.order_manager = OrderManager()
        cls.risk_manager = RiskManager()
        cls.test_symbol = "GC=F"  # Gold futures for testing
        cls.test_price = 1950.50
        cls.test_quantity = 1.0

    def test_execute_buy_order(self):
        """Test executing a buy order"""
        print("\n🔍 Running test: Execute Buy Order")
        order = self.trade_executor.execute_trade(
            symbol=self.test_symbol,
            trade_type="BUY",
            price=self.test_price,
            quantity=self.test_quantity
        )
        self.assertIsNotNone(order, "❌ Buy order failed to execute.")
        self.assertEqual(order["trade_type"], "BUY", "❌ Trade type mismatch.")
        self.assertEqual(order["symbol"], self.test_symbol, "❌ Symbol mismatch.")
        self.assertGreater(order["executed_price"], 0, "❌ Execution price invalid.")

    def test_execute_sell_order(self):
        """Test executing a sell order"""
        print("\n🔍 Running test: Execute Sell Order")
        order = self.trade_executor.execute_trade(
            symbol=self.test_symbol,
            trade_type="SELL",
            price=self.test_price,
            quantity=self.test_quantity
        )
        self.assertIsNotNone(order, "❌ Sell order failed to execute.")
        self.assertEqual(order["trade_type"], "SELL", "❌ Trade type mismatch.")
        self.assertEqual(order["symbol"], self.test_symbol, "❌ Symbol mismatch.")
        self.assertGreater(order["executed_price"], 0, "❌ Execution price invalid.")

    def test_risk_checks(self):
        """Test if the trade is allowed based on risk management settings"""
        print("\n🔍 Running test: Risk Management Check")
        risk_check = self.risk_manager.evaluate_trade_risk(
            symbol=self.test_symbol,
            trade_type="BUY",
            price=self.test_price,
            quantity=self.test_quantity
        )
        self.assertTrue(risk_check, "❌ Risk management blocked the trade incorrectly.")

    def test_order_placement(self):
        """Test if the order is correctly placed in the Order Manager"""
        print("\n🔍 Running test: Order Placement")
        order_id = self.order_manager.place_order(
            symbol=self.test_symbol,
            trade_type="BUY",
            price=self.test_price,
            quantity=self.test_quantity
        )
        self.assertIsNotNone(order_id, "❌ Order placement failed.")
        self.assertTrue(self.order_manager.order_exists(order_id), "❌ Order ID not found.")

    def test_invalid_trade_execution(self):
        """Test if invalid trades are rejected"""
        print("\n🔍 Running test: Invalid Trade Execution")
        invalid_order = self.trade_executor.execute_trade(
            symbol=self.test_symbol,
            trade_type="INVALID",
            price=self.test_price,
            quantity=self.test_quantity
        )
        self.assertIsNone(invalid_order, "❌ Invalid trade should not be executed.")

    def test_trade_logging(self):
        """Test if trades are correctly logged"""
        print("\n🔍 Running test: Trade Logging")
        order = self.trade_executor.execute_trade(
            symbol=self.test_symbol,
            trade_type="BUY",
            price=self.test_price,
            quantity=self.test_quantity
        )
        with open("logs/trade_logs.txt", "r") as log_file:
            logs = log_file.readlines()
        self.assertTrue(any(str(order["order_id"]) in log for log in logs), "❌ Trade log missing.")

if __name__ == "__main__":
    unittest.main()

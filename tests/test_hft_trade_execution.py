import unittest
import json
import time
from core.hft_trade_execution import HFTTradeExecution

class TestHFTTradeExecution(unittest.TestCase):
    """ Unit tests for AI-powered high-frequency trade execution """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize HFTTradeExecution """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.hft_executor = HFTTradeExecution(cls.config)

    def test_hft_order_execution_speed(self):
        """ Ensure AI executes HFT orders with minimal latency """
        test_order = {
            "symbol": "BTCUSDT",
            "order_type": "MARKET",
            "quantity": 1
        }

        start_time = time.time()
        execution_result = self.hft_executor.execute_hft_trade(test_order)
        execution_time = time.time() - start_time

        self.assertTrue(execution_result, "HFT order execution should be successful")
        self.assertLess(execution_time, 0.05, "HFT execution should be completed in under 50ms")

    def test_bid_ask_spread_optimization(self):
        """ Validate AI optimizes trade execution based on bid-ask spread """
        market_data = {
            "symbol": "ETHUSDT",
            "bid_price": 3200.50,
            "ask_price": 3201.00
        }

        optimized_order = self.hft_executor.optimize_execution_based_on_spread(market_data)

        self.assertIsInstance(optimized_order, dict, "Optimized order data should be a dictionary")
        self.assertGreaterEqual(optimized_order["execution_price"], market_data["bid_price"], "Execution price should be within spread")
        self.assertLessEqual(optimized_order["execution_price"], market_data["ask_price"], "Execution price should be optimized within spread")

    def test_hft_slippage_control(self):
        """ Ensure AI minimizes slippage in high-frequency trades """
        test_trade = {
            "symbol": "XAUUSD",
            "entry_price": 1850,
            "volume": 2
        }

        execution_data = self.hft_executor.control_hft_slippage(test_trade)

        self.assertIsInstance(execution_data, dict, "Execution data should return a dictionary")
        self.assertGreaterEqual(execution_data["adjusted_price"], 0, "Adjusted price should be valid")
        self.assertLessEqual(abs(execution_data["adjusted_price"] - test_trade["entry_price"]), test_trade["entry_price"] * self.hft_executor.slippage_tolerance, "Slippage should be within AI-defined limits")

    def test_market_depth_adaptation(self):
        """ Validate AI adapts trade execution based on market depth """
        order_book_data = {
            "BTCUSDT": {"total_bids": 1500, "total_asks": 1800}
        }

        market_adjustment = self.hft_executor.adapt_to_market_depth("BTCUSDT", order_book_data)

        self.assertIsInstance(market_adjustment, dict, "Market depth adjustment should return a dictionary")
        self.assertGreaterEqual(market_adjustment["execution_priority"], 0, "Execution priority should be non-negative")

    def test_hft_execution_log_integration(self):
        """ Ensure AI logs HFT trade execution for analysis """
        test_trade = {
            "symbol": "PL=F",
            "execution_time": "2025-02-20 20:00:00",
            "execution_price": 1120
        }

        log_result = self.hft_executor.log_hft_trade_execution(test_trade)

        self.assertTrue(log_result, "AI should successfully log HFT trade execution details")

if __name__ == "__main__":
    unittest.main()

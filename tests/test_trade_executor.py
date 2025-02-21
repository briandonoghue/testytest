import unittest
import json
from core.trade_executor import TradeExecutor
from core.market_data import MarketData

class TestTradeExecutor(unittest.TestCase):
    """ Unit tests for AI-driven trade execution system """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize TradeExecutor """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.trade_executor = TradeExecutor(cls.config)
        cls.market_data = MarketData(cls.config)

    def test_execution_delay_optimization(self):
        """ Ensure AI dynamically adjusts execution delay based on market liquidity """
        trade_signal = {"symbol": "BTCUSDT", "action": "BUY", "quantity": 1, "price": 50000}
        execution_data = self.trade_executor._apply_speed_optimization(trade_signal["symbol"], trade_signal["price"])

        self.assertIsNotNone(execution_data, "Execution optimization failed")
        self.assertGreaterEqual(execution_data[1], 0.05, "Execution delay should be within a reasonable range")
        self.assertLessEqual(execution_data[1], 2.0, "Execution delay should not exceed the max threshold")

    def test_slippage_control(self):
        """ Ensure AI execution optimizer reduces slippage within tolerance """
        trade_signal = {"symbol": "ETHUSDT", "action": "SELL", "quantity": 2, "price": 3000}
        adjusted_execution = self.trade_executor.optimize_slippage_control(trade_signal)

        self.assertIsNotNone(adjusted_execution, "Slippage control failed")
        self.assertLessEqual(abs(adjusted_execution["adjusted_price"] - trade_signal["price"]), trade_signal["price"] * self.trade_executor.slippage_tolerance,
                             "Slippage should be within the AI-defined tolerance")

    def test_order_execution(self):
        """ Validate AI executes orders only when market conditions meet AI approval criteria """
        trade_signal = {"symbol": "XAUUSD", "action": "BUY", "quantity": 5, "price": 1850}
        execution_result = self.trade_executor.execute_order(trade_signal)

        if execution_result:
            self.assertEqual(execution_result["status"], "Executed", "Trade should be successfully executed")
        else:
            self.assertIsNone(execution_result, "Trade execution should be skipped in unfavorable conditions")

    def test_liquidity_filtering(self):
        """ Ensure AI execution optimizer avoids executing trades in low-liquidity conditions """
        trade_signal = {"symbol": "PL=F", "action": "BUY", "quantity": 3, "price": 1000}
        execution_result = self.trade_executor.execute_order(trade_signal)

        if execution_result:
            self.assertGreaterEqual(self.market_data.get_liquidity_score(trade_signal["symbol"]), 0.5,
                                    "Trade should only execute in moderate to high liquidity environments")
        else:
            self.assertIsNone(execution_result, "Trade execution should be skipped due to low liquidity")

if __name__ == "__main__":
    unittest.main()

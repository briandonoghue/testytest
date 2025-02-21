import unittest
import json
from core.risk_manager import RiskManager
from core.market_data import MarketData

class TestRiskManager(unittest.TestCase):
    """ Unit tests for AI-driven risk management system """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize RiskManager """
        with open("config/risk_settings.json", "r") as f:
            cls.config = json.load(f)

        cls.risk_manager = RiskManager(cls.config)
        cls.market_data = MarketData(cls.config)

    def test_stop_loss_calculation(self):
        """ Ensure AI correctly calculates stop-loss levels """
        trade_signal = {"symbol": "BTCUSDT", "price": 50000, "quantity": 1}
        adjusted_trade = self.risk_manager.analyze_trade_risk(trade_signal)

        self.assertIsNotNone(adjusted_trade, "Trade risk analysis failed")
        self.assertGreater(adjusted_trade["stop_loss"], 0, "Stop-loss should be positive")
        self.assertLess(adjusted_trade["stop_loss"], trade_signal["price"], "Stop-loss should be below entry price")

    def test_take_profit_calculation(self):
        """ Ensure AI correctly calculates take-profit levels """
        trade_signal = {"symbol": "ETHUSDT", "price": 3000, "quantity": 2}
        adjusted_trade = self.risk_manager.analyze_trade_risk(trade_signal)

        self.assertIsNotNone(adjusted_trade, "Trade risk analysis failed")
        self.assertGreater(adjusted_trade["take_profit"], trade_signal["price"], "Take-profit should be above entry price")

    def test_dynamic_risk_adjustment(self):
        """ Validate AI adapts risk levels based on market volatility """
        portfolio_allocation = {
            "BTCUSDT": 40.0,
            "ETHUSDT": 30.0,
            "XAUUSD": 15.0,
            "PL=F": 15.0
        }

        adjusted_allocation = self.risk_manager.adjust_risk_levels(portfolio_allocation)

        for asset, allocation in adjusted_allocation.items():
            self.assertLessEqual(allocation, portfolio_allocation[asset], "Risk-adjusted allocation should not exceed original")

    def test_rebalancing_logic(self):
        """ Ensure AI correctly triggers rebalancing when required """
        portfolio_allocation = {
            "BTCUSDT": 50.0,  # High allocation
            "ETHUSDT": 20.0,
            "XAUUSD": 10.0,
            "PL=F": 20.0
        }

        rebalancing_orders = self.risk_manager.rebalance_portfolio()
        self.assertIsNotNone(rebalancing_orders, "Rebalancing should not return None")

        for order in rebalancing_orders:
            self.assertIn(order["symbol"], portfolio_allocation.keys(), "Rebalancing should only adjust existing assets")
            self.assertTrue(-0.1 <= order["adjustment"] <= 0.1, "Rebalancing adjustment should be within limits")

if __name__ == "__main__":
    unittest.main()

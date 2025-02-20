import unittest
from core.risk_manager import RiskManager

class TestRiskManager(unittest.TestCase):
    def setUp(self):
        """ Initializes RiskManager with default settings. """
        self.risk_manager = RiskManager(max_risk_per_trade=0.02, stop_loss_pct=0.01, take_profit_pct=0.03)

    def test_calculate_position_size_valid(self):
        """ Tests valid position size calculation. """
        portfolio_value = 100000
        trade_risk = 500
        position_size = self.risk_manager.calculate_position_size(portfolio_value, trade_risk)

        self.assertGreater(position_size, 0)
        self.assertLessEqual(position_size, portfolio_value * self.risk_manager.max_risk_per_trade / trade_risk)

    def test_calculate_position_size_invalid(self):
        """ Tests handling of invalid trade risk values. """
        portfolio_value = 100000
        trade_risk = -500  # Negative risk
        position_size = self.risk_manager.calculate_position_size(portfolio_value, trade_risk)

        self.assertEqual(position_size, 0)

    def test_apply_risk_controls_valid_order(self):
        """ Tests risk-adjusted order validation. """
        portfolio_value = 100000
        order = {"symbol": "XAUUSD", "quantity": 10, "price": 2100.00, "type": "buy"}
        adjusted_order = self.risk_manager.apply_risk_controls(order, portfolio_value)

        self.assertIsNotNone(adjusted_order)
        self.assertGreater(adjusted_order["stop_loss"], 0)
        self.assertGreater(adjusted_order["take_profit"], 0)

    def test_apply_risk_controls_exceeds_risk(self):
        """ Tests handling of trades exceeding risk limits. """
        portfolio_value = 10000
        order = {"symbol": "XAUUSD", "quantity": 500, "price": 2100.00, "type": "buy"}  # Too large

        adjusted_order = self.risk_manager.apply_risk_controls(order, portfolio_value)

        self.assertIsNotNone(adjusted_order)
        self.assertLessEqual(adjusted_order["quantity"], portfolio_value * self.risk_manager.max_risk_per_trade)

if __name__ == "__main__":
    unittest.main()

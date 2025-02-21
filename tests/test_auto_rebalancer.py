import unittest
import json
from core.auto_rebalancer import AutoRebalancer

class TestAutoRebalancer(unittest.TestCase):
    """ Unit tests for AI-powered portfolio auto-rebalancing """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize AutoRebalancer """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.rebalancer = AutoRebalancer(cls.config)

    def test_portfolio_rebalancing(self):
        """ Ensure AI correctly rebalances portfolio allocations """
        test_allocation = {
            "BTCUSDT": 55.0,  # Overallocated
            "ETHUSDT": 20.0,
            "XAUUSD": 15.0,
            "PL=F": 10.0
        }

        adjusted_allocation = self.rebalancer.rebalance(test_allocation)

        self.assertIsInstance(adjusted_allocation, dict, "Rebalanced allocation should be a dictionary")
        self.assertLessEqual(adjusted_allocation["BTCUSDT"], 50, "Overallocated assets should be reduced")
        self.assertGreaterEqual(sum(adjusted_allocation.values()), 99, "Total allocation should remain valid")

    def test_risk_control_in_rebalancing(self):
        """ Validate AI integrates risk control when rebalancing """
        portfolio_state = {
            "BTCUSDT": {"allocation": 60.0, "volatility": 0.08, "momentum": -0.04},
            "ETHUSDT": {"allocation": 15.0, "volatility": 0.04, "momentum": 0.02},
            "XAUUSD": {"allocation": 10.0, "volatility": 0.02, "momentum": 0.01},
            "PL=F": {"allocation": 15.0, "volatility": 0.05, "momentum": -0.01}
        }

        risk_adjusted_allocation = self.rebalancer.integrate_risk_management(portfolio_state)

        self.assertIsInstance(risk_adjusted_allocation, dict, "AI should return a dictionary of adjusted allocations")
        self.assertLessEqual(risk_adjusted_allocation["BTCUSDT"], 50, "Risky asset allocation should be reduced")
        self.assertGreaterEqual(risk_adjusted_allocation["XAUUSD"], 10, "Stable assets should be prioritized")

    def test_liquidity_aware_rebalancing(self):
        """ Ensure AI adjusts allocations based on asset liquidity """
        liquidity_data = {
            "BTCUSDT": 0.9,
            "ETHUSDT": 0.8,
            "XAUUSD": 0.6,
            "PL=F": 0.4
        }

        new_allocation = self.rebalancer.liquidity_adjustment(liquidity_data)

        self.assertIsInstance(new_allocation, dict, "Liquidity-adjusted allocation should be a dictionary")
        self.assertGreaterEqual(new_allocation["BTCUSDT"], 40, "High-liquidity assets should have stable allocation")
        self.assertLessEqual(new_allocation["PL=F"], 10, "Low-liquidity assets should be limited")

    def test_rebalancing_thresholds(self):
        """ Validate AI triggers rebalancing only when necessary """
        test_allocation = {
            "BTCUSDT": 51.0,  # Slightly overallocated
            "ETHUSDT": 19.0,
            "XAUUSD": 15.0,
            "PL=F": 15.0
        }

        should_rebalance = self.rebalancer.check_rebalancing_threshold(test_allocation)

        self.assertFalse(should_rebalance, "AI should not trigger rebalancing for minor deviations")

    def test_log_rebalancing_decisions(self):
        """ Ensure AI logs rebalancing actions for transparency """
        test_allocation = {
            "BTCUSDT": 50.0,
            "ETHUSDT": 20.0,
            "XAUUSD": 15.0,
            "PL=F": 15.0
        }

        log_result = self.rebalancer.log_rebalancing(test_allocation)

        self.assertTrue(log_result, "AI should successfully log rebalancing actions")

if __name__ == "__main__":
    unittest.main()

import unittest
import json
from core.portfolio_manager import PortfolioManager

class TestPortfolioManager(unittest.TestCase):
    """ Unit tests for AI-powered portfolio rebalancing system """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize PortfolioManager """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.portfolio_manager = PortfolioManager(cls.config)

    def test_portfolio_allocation(self):
        """ Ensure AI correctly allocates portfolio based on risk profile """
        portfolio_allocation = self.portfolio_manager.get_portfolio_allocation()

        self.assertIsInstance(portfolio_allocation, dict, "Portfolio allocation should return a dictionary")
        self.assertGreaterEqual(sum(portfolio_allocation.values()), 99, "Total allocation should be approximately 100%")

    def test_rebalancing_thresholds(self):
        """ Validate AI triggers rebalancing only when thresholds are met """
        test_allocation = {
            "BTCUSDT": 50.0,  # Overweighted
            "ETHUSDT": 20.0,
            "XAUUSD": 15.0,
            "PL=F": 15.0
        }

        rebalancing_actions = self.portfolio_manager.rebalance_portfolio(test_allocation)

        self.assertIsInstance(rebalancing_actions, list, "Rebalancing actions should return a list")
        self.assertGreaterEqual(len(rebalancing_actions), 1, "AI should generate at least one rebalancing action")
        self.assertIn("symbol", rebalancing_actions[0], "Rebalancing action should include asset symbol")

    def test_risk_exposure_reduction(self):
        """ Ensure AI reduces exposure to high-risk assets when necessary """
        high_risk_allocation = {
            "BTCUSDT": 70.0,  # Excessive allocation
            "ETHUSDT": 10.0,
            "XAUUSD": 10.0,
            "PL=F": 10.0
        }

        adjusted_portfolio = self.portfolio_manager.adjust_risk_exposure(high_risk_allocation)

        self.assertLessEqual(adjusted_portfolio["BTCUSDT"], 50, "High-risk asset allocation should be reduced")
        self.assertGreaterEqual(sum(adjusted_portfolio.values()), 99, "Total allocation should remain valid")

    def test_dynamic_market_adjustments(self):
        """ Validate AI dynamically adjusts portfolio based on market conditions """
        market_data = {
            "BTCUSDT": {"volatility": 0.08, "momentum": -0.03},
            "ETHUSDT": {"volatility": 0.04, "momentum": 0.02},
            "XAUUSD": {"volatility": 0.02, "momentum": 0.01},
            "PL=F": {"volatility": 0.06, "momentum": -0.01}
        }

        adjusted_allocations = self.portfolio_manager.optimize_portfolio(market_data)

        self.assertIsInstance(adjusted_allocations, dict, "AI should return adjusted portfolio allocations")
        self.assertGreaterEqual(adjusted_allocations["XAUUSD"], 10, "Gold allocation should be stable in high volatility periods")
        self.assertLessEqual(adjusted_allocations["BTCUSDT"], 45, "Crypto allocation should be adjusted due to momentum drop")

    def test_ai_auto_rebalancing(self):
        """ Ensure AI automatically rebalances when required """
        portfolio_allocation = {
            "BTCUSDT": 55.0,  # Overweighted
            "ETHUSDT": 15.0,
            "XAUUSD": 20.0,
            "PL=F": 10.0
        }

        rebalancing_orders = self.portfolio_manager.auto_rebalance(portfolio_allocation)

        self.assertIsInstance(rebalancing_orders, list, "AI should return rebalancing orders")
        self.assertGreaterEqual(len(rebalancing_orders), 1, "AI should generate at least one rebalancing action")

if __name__ == "__main__":
    unittest.main()

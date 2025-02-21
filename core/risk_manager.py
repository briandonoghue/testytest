import logging
import numpy as np
from utilities.config_loader import load_config
from core.market_data import MarketData
from core.performance_tracker import PerformanceTracker

class RiskManager:
    """ AI-driven risk management and portfolio rebalancing system """

    def __init__(self, config):
        """
        Initializes the risk manager with AI-based portfolio rebalancing.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.performance_tracker = PerformanceTracker(config)
        self.max_drawdown = config["risk_management"].get("max_drawdown", 5)  # Max loss percentage per asset
        self.auto_rebalance = config["bot_settings"].get("enable_auto_rebalance", True)
        self.rebalance_threshold = config["risk_management"].get("rebalance_threshold", 10)  # % deviation threshold

        # Setup logging
        logging.basicConfig(
            filename="logs/risk_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def evaluate_risk(self, trade_signal):
        """
        Assesses the risk level of a trade before execution.
        :param trade_signal: Trade signal dictionary.
        :return: True if the trade passes risk assessment, False otherwise.
        """
        symbol = trade_signal["symbol"]
        quantity = trade_signal["quantity"]
        current_price = self.market_data.get_latest_price(symbol)

        if current_price is None:
            logging.warning(f"Risk assessment failed: Market data unavailable for {symbol}")
            return False

        # Calculate position value
        position_value = quantity * current_price

        # Check max drawdown limits
        past_performance = self.performance_tracker.get_trade_log()
        recent_losses = sum([trade["execution_price"] for trade in past_performance if trade["symbol"] == symbol and trade["pnl"] < 0])
        if abs(recent_losses) > self.max_drawdown:
            logging.warning(f"Trade rejected: {symbol} exceeds max drawdown limit.")
            return False

        logging.info(f"Trade approved: {symbol} passes risk assessment.")
        return True

    def analyze_portfolio_allocation(self):
        """
        Analyzes portfolio allocation across different assets.
        :return: Dictionary of asset allocations.
        """
        trade_log = self.performance_tracker.get_trade_log()
        allocation = {}

        for trade in trade_log:
            if trade["symbol"] in allocation:
                allocation[trade["symbol"]] += abs(trade["execution_price"] * trade["quantity"])
            else:
                allocation[trade["symbol"]] = abs(trade["execution_price"] * trade["quantity"])

        total_portfolio_value = sum(allocation.values())

        # Normalize allocations as percentages
        allocation = {k: round((v / total_portfolio_value) * 100, 2) for k, v in allocation.items() if total_portfolio_value > 0}

        logging.info(f"Current Portfolio Allocation: {allocation}")
        return allocation

    def rebalance_portfolio(self):
        """
        Rebalances portfolio based on AI-driven analysis.
        """
        if not self.auto_rebalance:
            logging.info("AI-driven portfolio rebalancing is disabled.")
            return

        allocation = self.analyze_portfolio_allocation()
        ideal_allocation = self.config["risk_management"].get("ideal_allocation", {})

        rebalancing_orders = []
        for asset, current_allocation in allocation.items():
            if asset in ideal_allocation:
                deviation = abs(current_allocation - ideal_allocation[asset])
                if deviation > self.rebalance_threshold:
                    # Reduce or increase position to match ideal allocation
                    adjustment = (ideal_allocation[asset] - current_allocation) / 100
                    rebalancing_orders.append({"symbol": asset, "adjustment": adjustment})

        if rebalancing_orders:
            logging.info(f"Portfolio Rebalancing Orders: {rebalancing_orders}")
            return rebalancing_orders
        else:
            logging.info("No rebalancing needed at this time.")
            return None

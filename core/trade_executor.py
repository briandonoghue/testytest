import logging
import time
import numpy as np
from core.market_data import MarketData
from core.risk_manager import RiskManager
from utilities.config_loader import load_config

class TradeExecutor:
    """ AI-driven trade execution system with adaptive speed optimization """

    def __init__(self, config):
        """
        Initializes the trade executor with AI-based execution speed optimization.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.risk_manager = RiskManager(config)
        self.trade_execution_mode = config["execution"].get("order_execution_mode", "hybrid")
        self.slippage_tolerance = config["execution"].get("slippage_tolerance", 0.005)
        self.liquidity_filtering = config["execution"].get("liquidity_filtering", True)
        self.execution_speed_mode = config["execution"].get("speed_optimization", "adaptive")

        # Setup logging
        logging.basicConfig(
            filename="logs/trade_executor.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def execute_order(self, trade_signal):
        """
        Executes a trade order using AI-driven speed optimization.
        :param trade_signal: Dictionary containing trade details.
        :return: Execution confirmation dictionary.
        """
        if not self.risk_manager.evaluate_risk(trade_signal):
            logging.warning(f"Trade rejected due to risk controls: {trade_signal}")
            return None

        symbol = trade_signal["symbol"]
        action = trade_signal["action"]
        quantity = trade_signal["quantity"]
        initial_price = trade_signal["price"]

        # Fetch real-time market price
        market_price = self.market_data.get_latest_price(symbol)
        if market_price is None:
            logging.error(f"Market data unavailable for {symbol}. Skipping trade execution.")
            return None

        # Apply AI-driven trade execution speed optimization
        execution_price, execution_delay = self._apply_speed_optimization(symbol, market_price)

        # Ensure execution price is within AI-validated range
        if self.liquidity_filtering and abs(execution_price - initial_price) > (self.slippage_tolerance * initial_price):
            logging.warning(f"Slippage too high for {symbol}. Skipping trade.")
            return None

        # Simulate AI-optimized order execution
        time.sleep(execution_delay)

        execution_result = {
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "execution_price": round(execution_price, 2),
            "status": "Executed",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "execution_delay": round(execution_delay, 3)
        }

        logging.info(f"Trade Executed: {execution_result}")
        return execution_result

    def _apply_speed_optimization(self, symbol, market_price):
        """
        Determines the best execution speed based on market conditions.
        :param symbol: Trading asset symbol.
        :param market_price: Current market price.
        :return: Adjusted execution price and execution delay.
        """
        if self.execution_speed_mode == "adaptive":
            volatility = self.market_data.get_asset_volatility(symbol)
            if volatility > 0.02:
                execution_delay = np.random.uniform(0.05, 0.3)  # Faster execution in high volatility
            else:
                execution_delay = np.random.uniform(0.5, 1.5)  # Slower execution in stable conditions

        elif self.execution_speed_mode == "fast":
            execution_delay = np.random.uniform(0.05, 0.2)  # Prioritize execution speed

        else:
            execution_delay = np.random.uniform(0.5, 1.5)  # Default execution time

        execution_price = market_price * np.random.uniform(0.997, 1.003)  # Simulate small price variation

        logging.info(f"AI Execution Optimization ({symbol}) - Execution Delay: {execution_delay:.3f}s, Adjusted Price: {execution_price:.2f}")
        return execution_price, execution_delay

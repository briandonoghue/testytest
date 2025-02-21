import logging
import numpy as np
from core.trade_executor import TradeExecutor
from core.risk_manager import RiskManager
from ml.ai_strategy_optimizer import AIStrategyOptimizer

class OrderManager:
    """ Manages AI-driven trade execution and confidence-weighted position sizing. """

    def __init__(self, config):
        """
        Initializes the order manager.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.trade_executor = TradeExecutor(config)
        self.risk_manager = RiskManager(config)
        self.ai_optimizer = AIStrategyOptimizer(config)
        self.max_open_trades = config["trading_settings"].get("max_trades_per_cycle", 3)
        self.base_trade_size = config["bot_settings"].get("trade_size", 0.1)
        self.max_trade_risk = config["bot_settings"].get("max_trade_risk", 0.02)

        # Setup logging
        logging.basicConfig(
            filename="logs/order_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def _calculate_position_size(self, trade_signal):
        """
        Dynamically calculates trade size based on AI confidence.
        :param trade_signal: Trade signal dictionary.
        :return: Adjusted position size.
        """
        confidence = trade_signal.get("confidence", 0.5)  # Default confidence if missing

        # Scale trade size based on AI confidence
        trade_size = self.base_trade_size * (1 + (confidence - 0.5) * 2)

        # Ensure trade size does not exceed max trade risk
        max_allowed_size = self.max_trade_risk * self.config["bot_settings"].get("max_trade_risk", 0.02)
        adjusted_trade_size = min(trade_size, max_allowed_size)

        logging.info(f"AI-Weighted Position Size for {trade_signal['symbol']}: {adjusted_trade_size:.4f} (Confidence: {confidence:.2f})")
        return adjusted_trade_size

    def execute_trade_signal(self, trade_signal):
        """
        Validates and executes trade orders with AI-driven adjustments.
        :param trade_signal: Dictionary containing trade details.
        :return: Execution result or None if rejected.
        """
        if not trade_signal:
            logging.warning("Received an empty trade signal, skipping execution.")
            return None

        symbol = trade_signal["symbol"]
        action = trade_signal["action"]
        confidence = trade_signal.get("confidence", 0.5)

        # Risk evaluation
        if not self.risk_manager.evaluate_risk(trade_signal):
            logging.warning(f"Trade rejected due to risk controls: {trade_signal}")
            return None

        # Adjust trade size dynamically based on AI confidence
        trade_signal["quantity"] = self._calculate_position_size(trade_signal)

        # Execute trade
        execution_result = self.trade_executor.execute_order(trade_signal)
        if execution_result:
            logging.info(f"Trade Executed: {execution_result}")
            return execution_result

        logging.error(f"Trade execution failed for {symbol}.")
        return None

    def process_trade_batch(self, trade_signals):
        """
        Processes a batch of trade signals, prioritizing high-confidence trades.
        :param trade_signals: List of trade signal dictionaries.
        :return: List of executed trades.
        """
        if not trade_signals:
            logging.info("No trade signals to process.")
            return []

        # Sort trade signals by AI confidence score (highest first)
        trade_signals.sort(key=lambda x: x.get("confidence", 0), reverse=True)

        executed_trades = []
        for trade_signal in trade_signals[:self.max_open_trades]:  # Limit per cycle
            execution_result = self.execute_trade_signal(trade_signal)
            if execution_result:
                executed_trades.append(execution_result)

        logging.info(f"Processed {len(executed_trades)} trades this cycle.")
        return executed_trades

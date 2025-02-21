import logging
import pandas as pd
from core.market_data import MarketData
from ml.ai_strategy_optimizer import AIStrategyOptimizer
from strategies.adaptive_strategy import AdaptiveStrategy

class StrategyEngine:
    """ AI-driven strategy engine for trade signal generation. """

    def __init__(self, config, order_manager):
        """
        Initializes the strategy engine.
        :param config: Configuration dictionary.
        :param order_manager: Order management module instance.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.ai_optimizer = AIStrategyOptimizer(config)
        self.adaptive_strategy = AdaptiveStrategy(config)
        self.order_manager = order_manager
        self.confidence_threshold = config["strategies"]["adaptive"].get("ai_confidence_threshold", 0.7)

        # Setup logging
        logging.basicConfig(
            filename="logs/strategy_engine.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def generate_signals(self):
        """
        Generates AI-driven trade signals based on adaptive strategy learning.
        :return: List of validated trade signals.
        """
        logging.info("Generating AI-based trade signals...")

        # Fetch real-time market data
        market_df = self.market_data.get_historical_data("BTCUSDT", period="30d")

        if market_df.empty:
            logging.warning("No market data available. Skipping signal generation.")
            return []

        # Use AI model to predict best strategy and trade signals
        ai_trade_signal = self.ai_optimizer.generate_trade_signal(market_df)

        if not ai_trade_signal:
            logging.info("No AI trade signal generated. Skipping.")
            return []

        # Validate AI confidence level
        if ai_trade_signal["confidence"] < self.confidence_threshold:
            logging.warning(f"Trade signal confidence too low ({ai_trade_signal['confidence']:.2f}), skipping trade.")
            return []

        # Get trade signal from adaptive strategy
        adaptive_trade_signal = self.adaptive_strategy.generate_trade_signal(market_df)

        # Validate if AI-generated signal aligns with strategy-based signal
        if adaptive_trade_signal and ai_trade_signal["action"] == adaptive_trade_signal["action"]:
            logging.info(f"Final AI-validated trade signal: {ai_trade_signal}")
            return [ai_trade_signal]

        logging.warning("AI trade signal and adaptive strategy signal do not align. Skipping trade.")
        return []

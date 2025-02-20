import logging

class StrategyEngine:
    """ Generates trading signals based on predefined strategies. """

    def __init__(self, config, order_manager):
        """
        Initializes the strategy engine.

        :param config: Configuration dictionary.
        :param order_manager: Instance of OrderManager to execute trades.
        """
        self.config = config
        self.order_manager = order_manager

        # Setup logging
        logging.basicConfig(
            filename="logs/strategy_engine.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def generate_signals(self):
        """
        Generates trading signals based on strategy logic.

        :return: List of valid trade signals.
        """
        logging.info("Generating trading signals...")
        signals = []

        # Example: Basic Moving Average Crossover Strategy
        if self.config.get("strategy") == "moving_average":
            logging.info("Using Moving Average strategy...")
            
            trade_signal = {
                "symbol": "XAUUSD",
                "action": "buy",  # Ensure 'action' is present
                "price": 2100.00,  # Example price
                "quantity": 1
            }

            if all(key in trade_signal for key in ["symbol", "action", "price", "quantity"]):
                signals.append(trade_signal)
            else:
                logging.error("Invalid trade signal generated: %s", trade_signal)

        return signals

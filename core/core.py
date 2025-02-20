import os
import sys

# Ensure the core module can be imported correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
from market_data import MarketData
from config_loader import ConfigLoader
from strategy_manager import StrategyManager
from config_loader import ConfigLoader

class Core:
    """
    Core class to manage the initialization and execution of the Trading Bot.
    It serves as the central manager, initializing all key components and orchestrating the workflow.
    """
    def __init__(self):
        self.log = logging.Logger("Core")
        self.log.info("Initializing Trading Bot Core...")

        # Load configuration
        self.config = ConfigLoader().load_config()
        
        # Initialize components
        self.market_data = MarketData(self.config)
        # self.execution_engine = ExecutionEngine(self.config)
        self.strategy_manager = StrategyManager(self.config)

        self.log.info("All components initialized successfully.")

    def start(self):
        """
        Starts the trading bot.
        """
        self.log.info("Starting the Trading Bot...")

        # Fetch Market Data
        market_data = self.market_data.fetch_data()
        
        # Generate trading signals
        trading_signals = self.strategy_manager.generate_signals(market_data)
        
        # Execute trades based on signals
        self.execution_engine.execute_trades(trading_signals)

        self.log.info("Trading Bot Execution Completed.")

    def stop(self):
        """
        Stops the trading bot and performs cleanup.
        """
        self.log.info("Stopping Trading Bot... Cleaning up resources.")
        # Implement any cleanup logic if necessary
        self.log.info("Trading Bot Stopped Successfully.")

if __name__ == "__main__":
    bot = Core()
    bot.start()

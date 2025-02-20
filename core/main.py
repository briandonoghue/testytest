import logging
import sys
import os
import time  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from order_manager import OrderManager
from strategy_engine import StrategyEngine
from risk_manager import RiskManager
from backtester import Backtester
from utilities.config_loader import load_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

def main():
    logging.info("Starting Trading Bot...")

    try:
        config = load_config("config/config.json")

        if not config:
            logging.error("Configuration file is missing or invalid.")
            sys.exit(1)

        logging.info("Configuration loaded successfully.")

        order_manager = OrderManager(config)
        strategy_engine = StrategyEngine(config, order_manager)
        risk_manager = RiskManager(config)
        backtester = Backtester(config)

        logging.info("Running backtest...")
        backtester.run_backtest()
        logging.info("Backtesting completed.")

        logging.info("Starting test & training mode (No real trades)...")

        # 🔹 Disable Signal Generation While Setting Up
        disable_signals = config["bot_settings"].get("disable_signal_generation", True) 

        iteration = 0
        max_iterations = 100  # Stops bot after 100 cycles for testing
        while iteration < max_iterations:
            if disable_signals:
                logging.info(f"Iteration {iteration + 1} - Signal generation is disabled during setup.")
            else:
                logging.info(f"Iteration {iteration + 1} - Generating trading signals...")
                signals = strategy_engine.generate_signals()
                for signal in signals:
                    if risk_manager.evaluate_risk(signal):
                        logging.info(f"Simulated trade decision: {signal}")  # No real trades

            iteration += 1
            time.sleep(5)  # Prevents excessive logging

        logging.info("Training mode completed. Bot shutting down.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

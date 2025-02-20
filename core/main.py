import logging
import sys
import json
from core.order_manager import OrderManager
from core.strategy_engine import StrategyEngine
from core.risk_manager import RiskManager
from core.backtester import Backtester
from utilities.config_loader import load_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    logging.info("Starting Trading Bot...")
    
    try:
        # Load configuration securely
        config = load_config("config/config.json")
        
        # Validate configuration
        if not config:
            logging.error("Configuration file is missing or invalid.")
            sys.exit(1)
        
        logging.info("Configuration loaded successfully.")
        
        # Initialize trading components
        order_manager = OrderManager(config)
        strategy_engine = StrategyEngine(config)
        risk_manager = RiskManager(config)
        backtester = Backtester(config)
        
        logging.info("All modules initialized successfully.")
        
        # Backtesting before execution
        logging.info("Running backtesting...")
        backtester.run()
        logging.info("Backtesting completed.")
        
        # Main trading loop
        while True:
            try:
                # Fetch strategy recommendations
                trade_signal = strategy_engine.generate_signal()
                
                # Evaluate risk before execution
                if risk_manager.evaluate(trade_signal):
                    order_manager.execute_trade(trade_signal)
                    logging.info("Trade executed successfully.")
                else:
                    logging.info("Trade did not pass risk assessment. Skipping.")
            
            except Exception as e:
                logging.error(f"Error in trading loop: {e}", exc_info=True)
                continue  # Continue execution instead of stopping bot
            
    except KeyboardInterrupt:
        logging.info("Trading bot terminated by user.")
        sys.exit(0)
    
    except Exception as e:
        logging.critical(f"Fatal error in main execution: {e}", exc_info=True)
        sys.exit(1)
    
if __name__ == "__main__":
    main()

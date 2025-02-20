import logging
import os
from datetime import datetime

def setup_logging(log_dir="logs", log_level=logging.INFO):
    """
    Sets up logging for the trading bot.

    Args:
        log_dir (str): Directory where logs will be saved.
        log_level (int): Logging level (default: INFO).
    
    Returns:
        logging.Logger: Configured logger instance.
    """

    # Ensure log directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a unique log file name with timestamp
    log_filename = f"trading_bot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    log_filepath = os.path.join(log_dir, log_filename)

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filepath),  # Save to file
            logging.StreamHandler()  # Print to console
        ]
    )

    logger = logging.getLogger("TradingBot")
    logger.info("Logging initialized. Logs are stored in: %s", log_filepath)
    
    return logger

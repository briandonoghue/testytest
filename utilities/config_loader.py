import json
import logging
import os

class ConfigLoader:
    """ Handles loading and validation of the bot configuration file. """

    def __init__(self, config_path="config/config.json"):
        """
        Initializes the config loader.
        :param config_path: Path to the configuration file.
        """
        self.config_path = config_path
        self.config = {}

        # Setup logging
        logging.basicConfig(
            filename="logs/config_loader.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def load_config(self):
        """
        Loads the JSON configuration file and validates its structure.
        :return: Dictionary containing the validated configuration.
        """
        if not os.path.exists(self.config_path):
            logging.error(f"Configuration file not found: {self.config_path}")
            return self._default_config()

        try:
            with open(self.config_path, "r") as file:
                self.config = json.load(file)
                logging.info("Configuration loaded successfully.")
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing configuration file: {e}")
            return self._default_config()

        # Validate required keys
        required_keys = ["trading_settings", "api_keys", "risk_management", "bot_settings"]
        for key in required_keys:
            if key not in self.config:
                logging.warning(f"Missing key '{key}' in configuration. Using defaults.")
                self.config[key] = self._default_config().get(key)

        return self.config

    def _default_config(self):
        """
        Returns a default configuration if the file is missing or corrupt.
        """
        default_config = {
            "trading_settings": {
                "cycle_interval": 5,
                "max_trades_per_cycle": 3,
                "trade_execution_type": "market"
            },
            "api_keys": {
                "broker": "public",
                "data_provider": "public"
            },
            "risk_management": {
                "max_drawdown": 5,
                "stop_loss": 2,
                "take_profit": 4
            },
            "bot_settings": {
                "mode": "paper_trading",
                "logging_level": "INFO",
                "data_fetch_interval": 60
            }
        }
        logging.warning("Using default configuration due to missing or corrupt config file.")
        return default_config

# Utility function to load configuration
def load_config(config_path="config/config.json"):
    config_loader = ConfigLoader(config_path)
    return config_loader.load_config()

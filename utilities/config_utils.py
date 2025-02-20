import logging
import json
import os

class ConfigUtils:
    def __init__(self, config_file="config/config.json"):
        """
        Initializes the Config Utility.

        :param config_file: Path to the configuration file.
        """
        self.config_file = config_file
        self.config = self.load_config()

        # Setup logging
        logging.basicConfig(
            filename="logs/config_utils.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def load_config(self):
        """ Loads and validates the configuration file. """
        try:
            with open(self.config_file, "r") as file:
                config_data = json.load(file)

            if not isinstance(config_data, dict):
                raise ValueError("Invalid config format.")

            logging.info("Configuration loaded successfully.")
            return config_data

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            logging.error("Failed to load config: %s", e)
            return {}

    def get_config_value(self, key, default=None):
        """ Retrieves a config value, falling back to environment variables if missing. """
        return os.getenv(key.upper(), self.config.get(key, default))

# Example Usage
if __name__ == "__main__":
    config_util = ConfigUtils()

    api_key = config_util.get_config_value("api_key")
    print("API Key:", api_key)

    trade_limit = config_util.get_config_value("trade_limit", 1000)
    print("Trade Limit:", trade_limit)

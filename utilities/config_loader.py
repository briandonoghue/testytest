import json
import logging
import os

def load_config(config_path):
    """Loads configuration from a JSON file."""
    if not os.path.exists(config_path):
        logging.error(f"Configuration file not found: {config_path}")
        return None
    
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            logging.info("Configuration loaded successfully.")
            return config
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON configuration: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error loading config: {e}")
        return None

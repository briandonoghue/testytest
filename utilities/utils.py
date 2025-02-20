import os
import json
import logging
import pandas as pd
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename="logs/system_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class Utils:
    """Utility functions for file handling, logging, and data management"""

    @staticmethod
    def load_json(filepath):
        """Load a JSON file safely"""
        if not os.path.exists(filepath):
            logging.warning(f"⚠️ JSON file not found: {filepath}")
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            logging.error(f"❌ Failed to parse JSON file {filepath}: {e}")
            return None

    @staticmethod
    def save_json(filepath, data):
        """Save data to a JSON file"""
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            logging.info(f"✅ Successfully saved JSON file: {filepath}")
        except Exception as e:
            logging.error(f"❌ Failed to save JSON file {filepath}: {e}")

    @staticmethod
    def read_csv(filepath):
        """Read a CSV file into a DataFrame"""
        if not os.path.exists(filepath):
            logging.warning(f"⚠️ CSV file not found: {filepath}")
            return pd.DataFrame()
        try:
            return pd.read_csv(filepath, parse_dates=True, index_col=0)
        except Exception as e:
            logging.error(f"❌ Error reading CSV file {filepath}: {e}")
            return pd.DataFrame()

    @staticmethod
    def save_csv(filepath, df):
        """Save a DataFrame to a CSV file"""
        try:
            df.to_csv(filepath, index=True)
            logging.info(f"✅ Successfully saved CSV file: {filepath}")
        except Exception as e:
            logging.error(f"❌ Failed to save CSV file {filepath}: {e}")

    @staticmethod
    def log_event(message, level="info"):
        """Log an event to the system logs"""
        levels = {"info": logging.INFO, "warning": logging.WARNING, "error": logging.ERROR}
        logging.log(levels.get(level, logging.INFO), message)

    @staticmethod
    def get_current_timestamp():
        """Get the current timestamp in a readable format"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def ensure_directory_exists(directory):
        """Ensure that a directory exists, create it if not"""
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"📂 Created missing directory: {directory}")

    @staticmethod
    def format_currency(value):
        """Format a number as a currency string"""
        try:
            return f"${value:,.2f}"
        except (TypeError, ValueError):
            logging.error(f"❌ Error formatting currency for value: {value}")
            return "$0.00"

    @staticmethod
    def validate_api_keys(api_keys):
        """Validate API keys to ensure they are properly set"""
        missing_keys = [key for key, value in api_keys.items() if not value]
        if missing_keys:
            logging.warning(f"⚠️ Missing API keys: {', '.join(missing_keys)}")
            return False
        return True

# Ensure necessary directories exist on startup
Utils.ensure_directory_exists("logs")
Utils.ensure_directory_exists("data")

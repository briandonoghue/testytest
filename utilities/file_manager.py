import os
import json
import pandas as pd
from utilities.logger import Logger


class FileManager:
    """Handles file operations such as reading/writing JSON, CSV, and creating directories."""

    @staticmethod
    def ensure_directory_exists(directory):
        """Ensure that a directory exists, create it if not."""
        if not os.path.exists(directory):
            os.makedirs(directory)
            Logger.log_system(f"📂 Created missing directory: {directory}")

    @staticmethod
    def load_json(filepath):
        """Load a JSON file safely."""
        if not os.path.exists(filepath):
            Logger.log_error(f"⚠️ JSON file not found: {filepath}")
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            Logger.log_error(f"❌ Failed to parse JSON file {filepath}: {e}")
            return None

    @staticmethod
    def save_json(filepath, data):
        """Save data to a JSON file."""
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            Logger.log_system(f"✅ Successfully saved JSON file: {filepath}")
        except Exception as e:
            Logger.log_error(f"❌ Failed to save JSON file {filepath}: {e}")

    @staticmethod
    def read_csv(filepath):
        """Read a CSV file into a DataFrame."""
        if not os.path.exists(filepath):
            Logger.log_warning(f"⚠️ CSV file not found: {filepath}")
            return pd.DataFrame()
        try:
            return pd.read_csv(filepath, parse_dates=True, index_col=0)
        except Exception as e:
            Logger.log_error(f"❌ Error reading CSV file {filepath}: {e}")
            return pd.DataFrame()

    @staticmethod
    def save_csv(filepath, df):
        """Save a DataFrame to a CSV file."""
        try:
            df.to_csv(filepath, index=True)
            Logger.log_system(f"✅ Successfully saved CSV file: {filepath}")
        except Exception as e:
            Logger.log_error(f"❌ Failed to save CSV file {filepath}: {e}")

    @staticmethod
    def check_and_create_required_files():
        """Ensure required files exist and create them if missing."""
        required_files = {
            "config/config.json": "{}",
            "config/assets.json": "[]",
            "logs/trade_logs.txt": "🔍 Trade Log Initialized\n",
            "logs/error_logs.txt": "🔍 Error Log Initialized\n",
            "logs/system_logs.txt": "🔍 System Log Initialized\n",
            "logs/debug_logs.txt": "🔍 Debug Log Initialized\n",
            "data/paper_trading_results.csv": "Date,Asset,Action,Price,Quantity,Balance\n",
        }

        for filepath, default_content in required_files.items():
            if not os.path.exists(filepath):
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(default_content)
                Logger.log_system(f"📄 Created missing file: {filepath}")

# Ensure directories and files exist at startup
FileManager.ensure_directory_exists("logs")
FileManager.ensure_directory_exists("data")
FileManager.ensure_directory_exists("config")
FileManager.check_and_create_required_files()

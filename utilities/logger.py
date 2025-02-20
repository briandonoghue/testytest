import logging
import os
from datetime import datetime

class Logger:
    """Centralized logging system for tracking bot operations, errors, and performance"""

    LOG_DIRECTORY = "logs"
    LOG_FILES = {
        "trade": "trade_logs.txt",
        "error": "error_logs.txt",
        "system": "system_logs.txt",
        "debug": "debug_logs.txt"
    }

    @staticmethod
    def setup_logging():
        """Ensure logging directory and files exist before logging starts"""
        if not os.path.exists(Logger.LOG_DIRECTORY):
            os.makedirs(Logger.LOG_DIRECTORY)

        for log_file in Logger.LOG_FILES.values():
            log_path = os.path.join(Logger.LOG_DIRECTORY, log_file)
            if not os.path.exists(log_path):
                with open(log_path, "w") as file:
                    file.write(f"🔍 Log file initialized: {datetime.now()}\n")

    @staticmethod
    def log_event(message, log_type="system", level="info"):
        """
        Logs messages into the correct log file with timestamp.

        :param message: The log message
        :param log_type: One of ('trade', 'error', 'system', 'debug')
        :param level: Log level ('info', 'warning', 'error')
        """
        log_file = Logger.LOG_FILES.get(log_type, "system_logs.txt")
        log_path = os.path.join(Logger.LOG_DIRECTORY, log_file)

        levels = {
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR
        }

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}\n"

        try:
            with open(log_path, "a", encoding="utf-8") as file:
                file.write(log_entry)
        except Exception as e:
            print(f"❌ Failed to write

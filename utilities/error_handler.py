import logging
import os
import json
import traceback
from datetime import datetime

class ErrorHandler:
    """ Centralized error handling and logging system for AI trading bot """

    def __init__(self):
        """
        Initializes the error handler.
        """
        self.error_log_file = "logs/error_log.json"

        # Ensure log directory exists
        os.makedirs("logs", exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename="logs/system_health.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log_error(self, error_message, error_type="RuntimeError", source="Unknown"):
        """
        Logs an error to both system logs and structured JSON file.
        :param error_message: Description of the error.
        :param error_type: Category of error (e.g., APIError, ExecutionError, etc.).
        :param source: Component where the error occurred.
        """
        error_data = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "type": error_type,
            "source": source,
            "message": error_message
        }

        # Log error in system log
        logging.error(f"{error_type} in {source}: {error_message}")

        # Append error to JSON log file
        try:
            with open(self.error_log_file, "r") as f:
                error_log = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            error_log = []

        error_log.append(error_data)

        with open(self.error_log_file, "w") as f:
            json.dump(error_log, f, indent=4)

    def handle_exception(self, exception, source="Unknown"):
        """
        Handles exceptions by logging them properly.
        :param exception: The exception object.
        :param source: Component where the exception occurred.
        """
        error_message = "".join(traceback.format_exception(None, exception, exception.__traceback__))
        self.log_error(error_message, error_type="Exception", source=source)

    def get_recent_errors(self, limit=10):
        """
        Retrieves the most recent errors.
        :param limit: Number of recent errors to fetch.
        :return: List of recent error logs.
        """
        try:
            with open(self.error_log_file, "r") as f:
                error_log = json.load(f)
            return error_log[-limit:]  # Return last 'limit' errors
        except (FileNotFoundError, json.JSONDecodeError):
            return []

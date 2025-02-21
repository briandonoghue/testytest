import logging
import time
import traceback

class ErrorHandler:
    """ Handles errors, automatic retries, and failure alerts. """

    def __init__(self, max_retries=3, retry_delay=5):
        """
        Initializes the error handler.
        :param max_retries: Number of times to retry before logging a critical error.
        :param retry_delay: Seconds to wait before retrying.
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Setup logging
        logging.basicConfig(
            filename="logs/error_handling.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def handle_error(self, error, module_name="Unknown Module", function_name="Unknown Function", retry_function=None):
        """
        Logs the error and retries if necessary.
        :param error: Exception object.
        :param module_name: Name of the module where the error occurred.
        :param function_name: Name of the function where the error occurred.
        :param retry_function: Function to retry if the error allows it.
        """
        error_message = f"Error in {module_name}.{function_name}: {str(error)}"
        logging.error(error_message)
        logging.error(traceback.format_exc())

        # Retry mechanism for recoverable errors
        for attempt in range(1, self.max_retries + 1):
            logging.warning(f"Retrying ({attempt}/{self.max_retries}) after {self.retry_delay} seconds...")
            time.sleep(self.retry_delay)

            try:
                if retry_function:
                    return retry_function()
            except Exception as retry_error:
                logging.error(f"Retry attempt {attempt} failed: {str(retry_error)}")
                continue

        logging.critical(f"Max retries reached. Failed to recover from error in {module_name}.{function_name}")
        self.raise_alert(f"?? CRITICAL ERROR: {error_message}")

    def raise_alert(self, alert_message):
        """
        Sends an alert (could be extended to send emails, SMS, or push notifications).
        :param alert_message: Message to be sent in the alert.
        """
        logging.critical(f"ALERT: {alert_message}")
        print(f"?? CRITICAL ALERT: {alert_message} ??")

    def monitor_system_health(self):
        """
        Monitors key system processes and logs errors if anything fails.
        """
        logging.info("Performing system health check...")

        # Check database connectivity (placeholder for real checks)
        database_check = True
        api_check = True

        if not database_check:
            self.raise_alert("Database connection failed.")
        if not api_check:
            self.raise_alert("Market data API is unresponsive.")

        logging.info("System health check completed successfully.")

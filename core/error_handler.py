import logging
import time
import traceback
from notification_manager import NotificationManager

class ErrorHandler:
    def __init__(self, notification_manager):
        """
        Initializes the error handler.

        :param notification_manager: Instance of NotificationManager.
        """
        self.notification_manager = notification_manager

        # Setup logging
        logging.basicConfig(
            filename="logs/error_handler.log",
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log_error(self, error_message, level="ERROR"):
        """
        Logs an error and sends notifications if critical.

        :param error_message: Error description.
        :param level: Error level (INFO, WARNING, ERROR, CRITICAL).
        """
        formatted_error = f"[{level}] {error_message}"

        if level == "CRITICAL":
            logging.critical(formatted_error)
            self.notification_manager.send_notification(f"🚨 CRITICAL ERROR: {error_message}")
        elif level == "WARNING":
            logging.warning(formatted_error)
        else:
            logging.error(formatted_error)

    def handle_exception(self, exception, level="ERROR"):
        """
        Captures and logs full exception details.

        :param exception: Exception object.
        :param level: Error level (INFO, WARNING, ERROR, CRITICAL).
        """
        error_message = f"{type(exception).__name__}: {str(exception)}"
        error_trace = traceback.format_exc()
        full_error = f"{error_message}\n{error_trace}"

        self.log_error(full_error, level)

        if level == "CRITICAL":
            self.shutdown_bot()

    def shutdown_bot(self):
        """ Gracefully shuts down the bot on a fatal error. """
        logging.critical("🚨 Fatal error encountered. Shutting down the bot.")
        self.notification_manager.send_notification("🚨 Bot shutting down due to a critical error.")
        time.sleep(2)  # Allow time for notifications to send
        exit(1)

# Example Usage
if __name__ == "__main__":
    notification_manager = NotificationManager(email_enabled=True, sms_enabled=False)
    error_handler = ErrorHandler(notification_manager)

    try:
        # Simulate an error
        1 / 0  # Division by zero error
    except Exception as e:
        error_handler.handle_exception(e, level="CRITICAL")

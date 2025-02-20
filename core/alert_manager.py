import logging
import time
from notification_manager import NotificationManager

class AlertManager:
    def __init__(self, notification_manager, alert_cooldown=60):
        """
        Initializes the Alert Manager.

        :param notification_manager: Instance of NotificationManager.
        :param alert_cooldown: Minimum time (seconds) between duplicate alerts.
        """
        self.notification_manager = notification_manager
        self.alert_cooldown = alert_cooldown
        self.last_alert_times = {}

        # Setup logging
        logging.basicConfig(
            filename="logs/alert_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def send_alert(self, message, alert_type="INFO"):
        """
        Sends an alert if it hasn’t been triggered recently.

        :param message: Alert message.
        :param alert_type: Alert level (INFO, WARNING, CRITICAL).
        """
        current_time = time.time()

        if message in self.last_alert_times:
            if current_time - self.last_alert_times[message] < self.alert_cooldown:
                logging.info("Skipping duplicate alert: %s", message)
                return

        self.last_alert_times[message] = current_time
        alert_message = f"[{alert_type}] {message}"

        if alert_type == "CRITICAL":
            logging.critical(alert_message)
        elif alert_type == "WARNING":
            logging.warning(alert_message)
        else:
            logging.info(alert_message)

        self.notification_manager.send_notification(alert_message)

    def alert_price_spike(self, symbol, price, threshold):
        """ Alerts if a price spike exceeds the threshold. """
        message = f"?? {symbol} price spiked to {price}, exceeding {threshold}!"
        self.send_alert(message, alert_type="WARNING")

    def alert_trade_failure(self, order):
        """ Alerts if a trade execution fails. """
        message = f"? Trade execution failed: {order}"
        self.send_alert(message, alert_type="CRITICAL")

    def alert_drawdown(self, portfolio_value, max_drawdown):
        """ Alerts if the portfolio value drops below max drawdown limit. """
        message = f"?? Portfolio drawdown exceeded! Value: {portfolio_value}, Max Allowed: {max_drawdown}"
        self.send_alert(message, alert_type="CRITICAL")

# Example Usage
if __name__ == "__main__":
    notification_manager = NotificationManager(email_enabled=True, sms_enabled=False)
    alert_manager = AlertManager(notification_manager)

    # Simulate alerts
    alert_manager.alert_price_spike("XAUUSD", 2200, 2150)
    alert_manager.alert_trade_failure({"symbol": "XAUUSD", "quantity": 1, "price": 2100.00, "type": "buy"})
    alert_manager.alert_drawdown(45000, 50000)

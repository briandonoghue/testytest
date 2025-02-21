import unittest
import json
from utilities.notification_manager import NotificationManager

class TestNotificationManager(unittest.TestCase):
    """ Unit tests for AI-driven notification and alert system """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize NotificationManager """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.notification_manager = NotificationManager(cls.config)

    def test_trade_alerts(self):
        """ Ensure AI sends trade execution alerts correctly """
        test_trade = {
            "symbol": "BTCUSDT",
            "action": "BUY",
            "quantity": 1,
            "price": 50000
        }

        alert_result = self.notification_manager.send_trade_alert(test_trade)

        self.assertTrue(alert_result, "Trade alert should be successfully sent")

    def test_risk_alerts(self):
        """ Validate AI triggers risk warnings when necessary """
        test_risk_alert = {
            "symbol": "ETHUSDT",
            "message": "High volatility detected",
            "risk_level": "HIGH"
        }

        alert_result = self.notification_manager.send_risk_alert(test_risk_alert)

        self.assertTrue(alert_result, "Risk alert should be successfully sent")

    def test_error_alerts(self):
        """ Ensure AI correctly triggers error alerts for failures """
        test_error = {
            "source": "MarketData",
            "message": "API connection failed"
        }

        alert_result = self.notification_manager.send_error_alert(test_error)

        self.assertTrue(alert_result, "Error alert should be successfully sent")

    def test_alert_reliability(self):
        """ Validate AI alerts do not send duplicate messages """
        test_trade = {
            "symbol": "XAUUSD",
            "action": "SELL",
            "quantity": 2,
            "price": 1850
        }

        first_alert = self.notification_manager.send_trade_alert(test_trade)
        second_alert = self.notification_manager.send_trade_alert(test_trade)

        self.assertEqual(first_alert, second_alert, "Duplicate alerts should be prevented")

    def test_log_integration(self):
        """ Ensure AI notifications integrate with the logging system """
        test_log_entry = {
            "event": "Trade Executed",
            "symbol": "PL=F",
            "action": "BUY",
            "quantity": 1
        }

        log_result = self.notification_manager.log_notification(test_log_entry)

        self.assertTrue(log_result, "Log entry should be successfully recorded")

if __name__ == "__main__":
    unittest.main()

import logging
import smtplib
import os
import json
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ Setup logging
logger = logging.getLogger("Alerts")

class AlertManager:
    def __init__(self):
        """Initialize alerting system with email, SMS, and system notifications."""
        self.config = self.load_alert_config()
        self.email_enabled = self.config["email"]["enabled"]
        self.sms_enabled = self.config["sms"]["enabled"]
        self.push_enabled = self.config["push"]["enabled"]

        if self.sms_enabled:
            self.twilio_client = Client(self.config["sms"]["twilio_sid"], self.config["sms"]["twilio_auth_token"])

    @staticmethod
    def load_alert_config():
        """Load alert settings from the configuration file."""
        try:
            with open("config/alerts.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("⚠️ alerts.json not found! Using default alert settings.")
            return {
                "email": {"enabled": False, "smtp_server": "", "port": 587, "sender_email": "", "password": "", "recipient_email": ""},
                "sms": {"enabled": False, "twilio_sid": "", "twilio_auth_token": "", "twilio_number": "", "recipient_number": ""},
                "push": {"enabled": False}
            }

    def send_email_alert(self, subject, message):
        """Send email alerts for trading activity or errors."""
        if not self.email_enabled:
            return
        
        try:
            msg = MIMEMultipart()
            msg["From"] = self.config["email"]["sender_email"]
            msg["To"] = self.config["email"]["recipient_email"]
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP(self.config["email"]["smtp_server"], self.config["email"]["port"]) as server:
                server.starttls()
                server.login(self.config["email"]["sender_email"], self.config["email"]["password"])
                server.sendmail(self.config["email"]["sender_email"], self.config["email"]["recipient_email"], msg.as_string())

            logger.info(f"📧 Email alert sent: {subject}")
        except Exception as e:
            logger.error(f"❌ Email alert failed: {str(e)}")

    def send_sms_alert(self, message):
        """Send SMS alerts for urgent trading signals."""
        if not self.sms_enabled:
            return
        
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=self.config["sms"]["twilio_number"],
                to=self.config["sms"]["recipient_number"]
            )
            logger.info(f"📱 SMS alert sent: {message}")
        except Exception as e:
            logger.error(f"❌ SMS alert failed: {str(e)}")

    def system_notification(self, message):
        """Send push notification alerts to the system."""
        if self.push_enabled:
            logger.info(f"🔔 System Notification: {message}")
            os.system(f'notify-send "Trading Bot Alert" "{message}"')  # Linux/macOS
            os.system(f'powershell -Command "New-BurntToastNotification -Text \'Trading Bot Alert\', \'{message}\'"')  # Windows

    def send_trade_alert(self, asset, action, price, balance):
        """Send alerts for executed trades."""
        message = f"🚀 {action.upper()} EXECUTED | {asset} at ${price:.2f} | New Balance: ${balance:.2f}"
        self.send_email_alert("Trade Executed", message)
        self.send_sms_alert(message)
        self.system_notification(message)
        logger.info(message)

    def send_risk_alert(self, risk_type, details):
        """Send alerts when risk thresholds are triggered."""
        message = f"⚠️ RISK ALERT: {risk_type} - {details}"
        self.send_email_alert("Risk Alert", message)
        self.send_sms_alert(message)
        self.system_notification(message)
        logger.warning(message)

    def send_error_alert(self, error_message):
        """Send alerts for critical errors."""
        message = f"❌ SYSTEM ERROR: {error_message}"
        self.send_email_alert("Trading Bot Error", message)
        self.send_sms_alert(message)
        self.system_notification(message)
        logger.error(message)

# ✅ Example usage
if __name__ == "__main__":
    alerts = AlertManager()
    alerts.send_trade_alert("Gold", "BUY", 1925.30, 10400.50)
    alerts.send_risk_alert("Max Drawdown Exceeded", "Account balance dropped by 10%")
    alerts.send_error_alert("API connection lost!")

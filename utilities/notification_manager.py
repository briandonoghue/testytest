import logging
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utilities.config_loader import load_config

class NotificationManager:
    """ Handles real-time notifications for AI trade execution and risk alerts. """

    def __init__(self, config):
        """
        Initializes the notification manager.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.email_enabled = config["notifications"].get("email_alerts", False)
        self.sms_enabled = config["notifications"].get("sms_alerts", False)
        self.webhook_enabled = config["notifications"].get("webhook_alerts", False)
        self.email_settings = config["notifications"].get("email_settings", {})
        self.sms_settings = config["notifications"].get("sms_settings", {})
        self.webhook_url = config["notifications"].get("webhook_url", "")

        # Setup logging
        logging.basicConfig(
            filename="logs/notification_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def send_trade_alert(self, trade_signal, execution_result):
        """
        Sends trade execution alerts with AI confidence level.
        :param trade_signal: Trade signal details.
        :param execution_result: Execution confirmation details.
        """
        message = f"""
        🚀 AI Trade Alert 🚀
        Symbol: {trade_signal["symbol"]}
        Action: {trade_signal["action"]}
        Quantity: {trade_signal["quantity"]}
        Execution Price: {execution_result["execution_price"]}
        AI Confidence: {trade_signal.get("confidence", 'N/A')}%
        Status: {execution_result["status"]}
        """
        logging.info(message)

        if self.email_enabled:
            self._send_email("AI Trade Alert", message)

        if self.sms_enabled:
            self._send_sms(message)

        if self.webhook_enabled:
            self._send_webhook(message)

    def send_risk_alert(self, symbol, risk_score):
        """
        Sends an alert when an extreme market event is detected.
        :param symbol: Trading asset symbol.
        :param risk_score: AI risk prediction score.
        """
        message = f"""
        ⚠️ Extreme Market Event Alert ⚠️
        Symbol: {symbol}
        AI-Predicted Risk Score: {risk_score}
        Suggested Action: Review AI trade confidence and adjust risk exposure.
        """
        logging.warning(message)

        if self.email_enabled:
            self._send_email("AI Risk Alert", message)

        if self.sms_enabled:
            self._send_sms(message)

        if self.webhook_enabled:
            self._send_webhook(message)

    def _send_email(self, subject, message):
        """
        Sends an email alert.
        :param subject: Email subject.
        :param message: Email content.
        """
        try:
            smtp_server = self.email_settings["smtp_server"]
            smtp_port = self.email_settings["smtp_port"]
            sender_email = self.email_settings["sender_email"]
            receiver_email = self.email_settings["receiver_email"]
            email_password = self.email_settings["email_password"]

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            logging.info(f"Email notification sent: {subject}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

    def _send_sms(self, message):
        """
        Sends an SMS notification.
        :param message: SMS content.
        """
        try:
            sms_api_url = self.sms_settings["sms_api_url"]
            api_key = self.sms_settings["api_key"]
            phone_number = self.sms_settings["phone_number"]

            payload = {
                "to": phone_number,
                "message": message,
                "api_key": api_key
            }
            response = requests.post(sms_api_url, json=payload)
            response.raise_for_status()
            logging.info("SMS notification sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send SMS: {e}")

    def _send_webhook(self, message):
        """
        Sends a webhook notification.
        :param message: Webhook message.
        """
        try:
            payload = {"text": message}
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            logging.info("Webhook notification sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send webhook notification: {e}")

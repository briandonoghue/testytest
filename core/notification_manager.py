import logging
import threading
import smtplib
import os
from email.message import EmailMessage
from twilio.rest import Client

class NotificationManager:
    def __init__(self, email_enabled=True, sms_enabled=False):
        """
        Initializes the notification manager.

        :param email_enabled: Enables email notifications.
        :param sms_enabled: Enables SMS notifications (requires Twilio).
        """
        self.email_enabled = email_enabled
        self.sms_enabled = sms_enabled

        # Email Configuration (Uses Environment Variables for Security)
        self.email_sender = os.getenv("EMAIL_SENDER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_receiver = os.getenv("EMAIL_RECEIVER")

        # Twilio SMS Configuration (Optional)
        self.twilio_sid = os.getenv("TWILIO_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone = os.getenv("TWILIO_PHONE")
        self.sms_receiver = os.getenv("SMS_RECEIVER")

        # Setup logging
        logging.basicConfig(
            filename="logs/notification_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def send_notification(self, message):
        """
        Sends a notification via email or SMS.

        :param message: Notification message.
        """
        threading.Thread(target=self._send_email, args=(message,)).start()
        if self.sms_enabled:
            threading.Thread(target=self._send_sms, args=(message,)).start()

    def _send_email(self, message):
        """ Sends an email notification. """
        if not self.email_enabled or not self.email_sender:
            logging.warning("Email notifications are disabled or sender not configured.")
            return

        try:
            msg = EmailMessage()
            msg.set_content(message)
            msg["Subject"] = "Trading Bot Alert"
            msg["From"] = self.email_sender
            msg["To"] = self.email_receiver

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)

            logging.info("Email notification sent successfully.")
        except Exception as e:
            logging.error("Failed to send email: %s", e)

    def _send_sms(self, message):
        """ Sends an SMS notification using Twilio. """
        if not self.sms_enabled or not self.twilio_sid:
            logging.warning("SMS notifications are disabled or Twilio credentials not configured.")
            return

        try:
            client = Client(self.twilio_sid, self.twilio_auth_token)
            client.messages.create(
                body=message,
                from_=self.twilio_phone,
                to=self.sms_receiver
            )
            logging.info("SMS notification sent successfully.")
        except Exception as e:
            logging.error("Failed to send SMS: %s", e)

# Example Usage
if __name__ == "__main__":
    notification_manager = NotificationManager(email_enabled=True, sms_enabled=False)
    
    # Send a test alert
    notification_manager.send_notification("Test alert: Your trading bot executed a trade.")

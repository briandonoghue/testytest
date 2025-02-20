import logging
import datetime
import pytz

class TimeUtils:
    def __init__(self, timezone="UTC"):
        """
        Initializes TimeUtils with a specific timezone.

        :param timezone: Timezone for market operations.
        """
        self.timezone = pytz.timezone(timezone)

        # Setup logging
        logging.basicConfig(
            filename="logs/time_utils.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def get_current_time(self):
        """ Returns the current time in the specified timezone. """
        return datetime.datetime.now(self.timezone)

    def convert_timestamp_to_datetime(self, timestamp):
        """ Converts a Unix timestamp to a formatted datetime string. """
        try:
            dt = datetime.datetime.fromtimestamp(timestamp, self.timezone)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logging.error("Error converting timestamp: %s", e)
            return None

    def calculate_time_difference(self, start_time, end_time):
        """ Calculates time difference between two timestamps. """
        try:
            delta = end_time - start_time
            return delta.total_seconds()
        except Exception as e:
            logging.error("Error calculating time difference: %s", e)
            return None

    def is_market_open(self, market_open="09:00", market_close="17:00"):
        """
        Checks if the current time is within market hours.

        :param market_open: Market opening time in HH:MM format.
        :param market_close: Market closing time in HH:MM format.
        :return: True if within market hours, False otherwise.
        """
        try:
            now = self.get_current_time()
            open_time = datetime.datetime.strptime(market_open, "%H:%M").time()
            close_time = datetime.datetime.strptime(market_close, "%H:%M").time()

            return open_time <= now.time() <= close_time
        except Exception as e:
            logging.error("Error checking market hours: %s", e)
            return False

# Example Usage
if __name__ == "__main__":
    time_utils = TimeUtils(timezone="UTC")

    print("Current Time:", time_utils.get_current_time())
    print("Timestamp to Datetime:", time_utils.convert_timestamp_to_datetime(1700000000))
    
    start = datetime.datetime(2024, 2, 1, 9, 0, tzinfo=pytz.UTC)
    end = datetime.datetime(2024, 2, 1, 16, 0, tzinfo=pytz.UTC)
    print("Time Difference (seconds):", time_utils.calculate_time_difference(start, end))

    print("Is Market Open?", time_utils.is_market_open())

import logging
import os
import json
import pandas as pd
from datetime import datetime

class TradeLogger:
    """ Handles logging of trade executions for analysis and debugging. """

    def __init__(self, log_dir="logs/"):
        """
        Initializes the trade logger.
        :param log_dir: Directory where logs are stored.
        """
        self.log_dir = log_dir
        self.log_file_json = os.path.join(log_dir, "trade_log.json")
        self.log_file_csv = os.path.join(log_dir, "trade_log.csv")

        os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(
            filename=os.path.join(log_dir, "trade_logger.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log_trade(self, trade_details):
        """
        Logs a successfully executed trade.
        :param trade_details: Dictionary containing trade execution details.
        """
        if not all(key in trade_details for key in ["symbol", "action", "quantity", "execution_price", "timestamp"]):
            logging.error("Trade log entry missing required fields.")
            return

        trade_details["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log to JSON
        self._log_to_json(trade_details)

        # Log to CSV
        self._log_to_csv(trade_details)

        logging.info(f"Trade logged: {trade_details}")

    def _log_to_json(self, trade_details):
        """
        Logs trade details to a JSON file.
        """
        trade_logs = []
        if os.path.exists(self.log_file_json):
            with open(self.log_file_json, "r") as f:
                try:
                    trade_logs = json.load(f)
                except json.JSONDecodeError:
                    logging.warning("Corrupt JSON log file detected. Resetting log.")

        trade_logs.append(trade_details)

        with open(self.log_file_json, "w") as f:
            json.dump(trade_logs, f, indent=4)

    def _log_to_csv(self, trade_details):
        """
        Logs trade details to a CSV file.
        """
        df = pd.DataFrame([trade_details])

        if not os.path.exists(self.log_file_csv):
            df.to_csv(self.log_file_csv, index=False, mode='w')
        else:
            df.to_csv(self.log_file_csv, index=False, header=False, mode='a')

    def get_trade_logs(self, format_type="json"):
        """
        Retrieves trade logs in the requested format.
        :param format_type: "json" or "csv".
        :return: Trade log data.
        """
        if format_type == "json" and os.path.exists(self.log_file_json):
            with open(self.log_file_json, "r") as f:
                return json.load(f)
        elif format_type == "csv" and os.path.exists(self.log_file_csv):
            return pd.read_csv(self.log_file_csv).to_dict(orient="records")
        return []

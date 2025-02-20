import logging
import threading
import pandas as pd
import os

class TradeLogger:
    def __init__(self, log_file="logs/trade_history.csv"):
        """
        Initializes the trade logger.

        :param log_file: Path to the CSV file storing trade history.
        """
        self.log_file = log_file

        # Setup logging for trade events
        logging.basicConfig(
            filename="logs/trade_logger.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # Ensure the CSV file has headers if it doesn't exist
        if not os.path.exists(self.log_file):
            pd.DataFrame(columns=["Timestamp", "Symbol", "Quantity", "Price", "Type", "Profit"]).to_csv(self.log_file, index=False)

    def log_trade(self, trade):
        """
        Logs a trade asynchronously.

        :param trade: Trade details (dict).
        """
        threading.Thread(target=self._log_trade_to_file, args=(trade,)).start()

    def _log_trade_to_file(self, trade):
        """
        Appends a trade to the CSV log file.

        :param trade: Trade details (dict).
        """
        try:
            trade_data = {
                "Timestamp": pd.Timestamp.now(),
                "Symbol": trade["symbol"],
                "Quantity": trade["quantity"],
                "Price": trade["price"],
                "Type": trade["type"],
                "Profit": trade.get("profit", 0)  # Default to 0 if not provided
            }

            df = pd.DataFrame([trade_data])
            df.to_csv(self.log_file, mode="a", header=False, index=False)

            logging.info("Trade logged: %s", trade_data)
        except Exception as e:
            logging.error("Failed to log trade: %s", e)

    def get_trade_history(self):
        """
        Fetches trade history from the CSV file.

        :return: Pandas DataFrame containing trade history.
        """
        try:
            df = pd.read_csv(self.log_file)
            return df
        except Exception as e:
            logging.error("Failed to load trade history: %s", e)
            return None

# Example Usage
if __name__ == "__main__":
    trade_logger = TradeLogger()

    # Simulate trade logging
    trade1 = {"symbol": "XAUUSD", "quantity": 2, "price": 2100.00, "type": "buy", "profit": 50.00}
    trade2 = {"symbol": "XAUUSD", "quantity": 1, "price": 2110.00, "type": "sell", "profit": -10.00}

    trade_logger.log_trade(trade1)
    trade_logger.log_trade(trade2)

    # Fetch and display trade history
    trade_history = trade_logger.get_trade_history()
    print("Trade History:\n", trade_history)

import logging
import pandas as pd

class Backtester:
    """ Simulates trading strategies on historical data """

    def __init__(self, config):
        """
        Initializes Backtester.

        :param config: Configuration dictionary.
        """
        self.config = config
        self.trade_log = []

        # Setup logging
        logging.basicConfig(
            filename="logs/backtester.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def record_trade(self, trade):
        """
        Logs a trade if it contains required fields.
        
        :param trade: Dictionary containing trade details.
        """
        required_fields = {"symbol", "action", "price", "quantity"}

        if not all(field in trade for field in required_fields):
            logging.error("Trade data missing required fields: %s", trade)
            return

        self.trade_log.append(trade)
        logging.info("Recorded trade: %s", trade)

    def run_backtest(self):
        """
        Simulates a backtest and ensures valid trade signals are processed.
        """
        logging.info("Running backtest...")

        if not self.trade_log:
            logging.warning("No trades to backtest.")
            return

        df = pd.DataFrame(self.trade_log)
        
        if "action" not in df.columns:
            logging.error("Trade log is missing 'action' column!")
            return

        total_profit = df[df["action"] == "sell"]["price"].sum() - df[df["action"] == "buy"]["price"].sum()
        logging.info("Backtest complete. Total Profit: %.2f", total_profit)
        print("\n📊 Backtest Summary 📊")
        print("Total Profit:", total_profit)
        print(df)

# Example Usage
if __name__ == "__main__":
    backtester = Backtester({"strategy": "moving_average"})

    # Simulating valid trades
    backtester.record_trade({"symbol": "XAUUSD", "action": "buy", "price": 2100.00, "quantity": 1})
    backtester.record_trade({"symbol": "XAUUSD", "action": "sell", "price": 2120.00, "quantity": 1})

    backtester.run_backtest()

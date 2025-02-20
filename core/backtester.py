import logging
import pandas as pd

class Backtester:
    """ Simulates trading strategies on historical data """

    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.trade_log = []

        # Setup logging
        logging.basicConfig(
            filename="logs/backtester.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def record_trade(self, symbol, action, price, quantity):
        """ Logs AI-generated trades for backtesting """
        trade = {
            "symbol": symbol,
            "action": action,
            "price": price,
            "quantity": quantity,
            "balance_after_trade": self.balance
        }
        self.trade_log.append(trade)
        logging.info("Paper Trade: %s %s at %.2f", action.upper(), symbol, price)

    def run_backtest(self):
        """ Simulates AI trading performance """
        df = pd.DataFrame(self.trade_log)
        total_profit = df[df["action"] == "sell"]["price"].sum() - df[df["action"] == "buy"]["price"].sum()
        
        logging.info("Backtest Complete. Total Profit: %.2f", total_profit)
        print("\n📊 Backtest Summary 📊")
        print("Total Profit:", total_profit)
        print(df)

# Example Usage
if __name__ == "__main__":
    backtester = Backtester()
    backtester.record_trade("XAUUSD", "buy", 2100.00, 1)
    backtester.record_trade("XAUUSD", "sell", 2120.00, 1)
    backtester.run_backtest()

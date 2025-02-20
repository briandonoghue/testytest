import logging
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
from market_data import MarketData
from position_manager import PositionManager

class TradingDashboard:
    def __init__(self, root, market_data, position_manager):
        """
        Initializes the trading dashboard.

        :param root: Tkinter root window.
        :param market_data: Instance of MarketData for live updates.
        :param position_manager: Instance of PositionManager for position tracking.
        """
        self.root = root
        self.market_data = market_data
        self.position_manager = position_manager
        self.root.title("Trading Bot Dashboard")
        self.root.geometry("800x600")

        # Live Price Display
        self.price_label = tk.Label(root, text="Live Price: Loading...", font=("Arial", 14))
        self.price_label.pack(pady=10)

        # Trade History Log
        self.trade_log = scrolledtext.ScrolledText(root, width=80, height=15)
        self.trade_log.pack(pady=10)
        self.trade_log.insert(tk.END, "Trade log initialized...\n")
        self.trade_log.config(state=tk.DISABLED)

        # Error Log Display
        self.error_log = scrolledtext.ScrolledText(root, width=80, height=5, fg="red")
        self.error_log.pack(pady=10)
        self.error_log.insert(tk.END, "Error log initialized...\n")
        self.error_log.config(state=tk.DISABLED)

        # Start background updates
        self.update_dashboard()

    def update_dashboard(self):
        """ Updates the dashboard with live market data and trade activity. """
        threading.Thread(target=self._update_price, daemon=True).start()
        threading.Thread(target=self._update_trade_log, daemon=True).start()
        threading.Thread(target=self._update_error_log, daemon=True).start()

    def _update_price(self):
        """ Updates live market price in UI. """
        while True:
            price = self.market_data.get_live_price("XAUUSD")
            self.price_label.config(text=f"Live Price: ${price:.2f}")
            time.sleep(5)

    def _update_trade_log(self):
        """ Updates trade history log dynamically. """
        while True:
            with open("logs/trade_history.csv", "r") as file:
                trades = file.readlines()

            self.trade_log.config(state=tk.NORMAL)
            self.trade_log.delete("1.0", tk.END)
            self.trade_log.insert(tk.END, "".join(trades[-10:]))  # Show last 10 trades
            self.trade_log.config(state=tk.DISABLED)
            time.sleep(5)

    def _update_error_log(self):
        """ Updates error log dynamically. """
        while True:
            with open("logs/error_handler.log", "r") as file:
                errors = file.readlines()

            self.error_log.config(state=tk.NORMAL)
            self.error_log.delete("1.0", tk.END)
            self.error_log.insert(tk.END, "".join(errors[-5:]))  # Show last 5 errors
            self.error_log.config(state=tk.DISABLED)
            time.sleep(5)

# Example Usage
if __name__ == "__main__":
    market_data = MarketData()
    position_manager = PositionManager(market_data, None)

    root = tk.Tk()
    dashboard = TradingDashboard(root, market_data, position_manager)
    root.mainloop()

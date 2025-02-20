import os
import json
import requests
import pandas as pd
from datetime import datetime

class TraderTracking:
    def __init__(self, trader_data_path="data/trader_data.json", top_traders_limit=100):
        """Initialize the Trader Tracking module."""
        self.trader_data_path = trader_data_path
        self.top_traders_limit = top_traders_limit
        self.traders = self.load_traders()

    def load_traders(self):
        """Load trader data from JSON file."""
        if os.path.exists(self.trader_data_path):
            with open(self.trader_data_path, "r") as f:
                return json.load(f)
        else:
            print(f"⚠️ No trader data found. Creating a new list.")
            return {"traders": []}

    def save_traders(self):
        """Save trader data to JSON file."""
        with open(self.trader_data_path, "w") as f:
            json.dump(self.traders, f, indent=4)
        print(f"✅ Trader data saved to {self.trader_data_path}")

    def fetch_trader_data(self, platform="binance"):
        """
        Fetch top trader data from public APIs.
        Supported Platforms: Binance, Crypto.com, Custom APIs.
        """
        if platform == "binance":
            url = "https://api.binance.com/api/v3/ticker/24hr"
        elif platform == "coingecko":
            url = "https://api.coingecko.com/api/v3/exchanges/binance"
        else:
            print(f"❌ Unsupported platform: {platform}")
            return None

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"❌ Failed to fetch data from {platform}. Status Code: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error fetching trader data: {e}")
            return None

    def filter_top_traders(self, data):
        """
        Filters the top traders based on trading volume and PnL.
        Assumes input is a list of trading data from the API.
        """
        if not data:
            print("⚠️ No data to filter.")
            return []

        df = pd.DataFrame(data)
        df["quoteVolume"] = pd.to_numeric(df["quoteVolume"], errors="coerce")
        df = df.sort_values(by="quoteVolume", ascending=False)
        
        top_traders = df.head(self.top_traders_limit).to_dict(orient="records")
        return top_traders

    def update_trader_list(self):
        """
        Fetches and updates the list of top traders dynamically.
        Stores their trading activity for learning.
        """
        print("🔍 Fetching latest top trader data...")
        data = self.fetch_trader_data("binance")
        if data:
            top_traders = self.filter_top_traders(data)
            self.traders["traders"] = top_traders
            self.save_traders()
            print(f"✅ Successfully updated top {self.top_traders_limit} traders.")
        else:
            print("❌ Failed to update trader list.")

    def monitor_trades(self):
        """Simulates monitoring top traders' activities for trade signals."""
        print("🔍 Monitoring top traders for trade signals...")

        if not self.traders["traders"]:
            print("⚠️ No traders found. Fetching new data...")
            self.update_trader_list()

        for trader in self.traders["traders"]:
            trader_id = trader.get("symbol", "Unknown")
            volume = trader.get("quoteVolume", 0)
            price_change = trader.get("priceChangePercent", 0)

            if float(price_change) > 5:
                print(f"📈 Potential buy signal detected for {trader_id} (+{price_change}% in 24h)")
            elif float(price_change) < -5:
                print(f"📉 Potential sell signal detected for {trader_id} ({price_change}% in 24h)")

    def run(self):
        """Runs the trader tracking module continuously."""
        self.update_trader_list()
        self.monitor_trades()


# ✅ Example Usage
if __name__ == "__main__":
    tracker = TraderTracking()
    tracker.run()

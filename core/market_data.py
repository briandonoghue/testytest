import logging
import requests
import time
import pandas as pd

class MarketData:
    def __init__(self, primary_source="yahoo", backup_source="binance", cache_expiry=60):
        """
        Initializes the market data module.

        :param primary_source: Primary data provider (e.g., "yahoo", "binance").
        :param backup_source: Backup provider in case of failures.
        :param cache_expiry: Cache expiry time in seconds.
        """
        self.primary_source = primary_source
        self.backup_source = backup_source
        self.cache_expiry = cache_expiry
        self.cache = {}  # Stores cached market data

        # Setup logging
        logging.basicConfig(
            filename="logs/market_data.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def get_live_price(self, symbol):
        """
        Fetches the latest price for a given symbol.

        :param symbol: Trading symbol (e.g., "XAUUSD").
        :return: Latest price or None if request fails.
        """
        if symbol in self.cache and time.time() - self.cache[symbol]["timestamp"] < self.cache_expiry:
            return self.cache[symbol]["price"]

        try:
            price = self._fetch_from_primary_source(symbol)
            if price is None:
                price = self._fetch_from_backup_source(symbol)
            
            if price:
                self.cache[symbol] = {"price": price, "timestamp": time.time()}
                logging.info("Fetched live price: %s = %.2f", symbol, price)
                return price
            else:
                logging.error("Failed to fetch live price for %s", symbol)
                return None

        except Exception as e:
            logging.error("Error fetching live price for %s: %s", symbol, e)
            return None

    def _fetch_from_primary_source(self, symbol):
        """ Fetch price from the primary data source """
        if self.primary_source == "yahoo":
            return self._fetch_yahoo(symbol)
        elif self.primary_source == "binance":
            return self._fetch_binance(symbol)
        return None

    def _fetch_from_backup_source(self, symbol):
        """ Fetch price from the backup data source """
        if self.backup_source == "yahoo":
            return self._fetch_yahoo(symbol)
        elif self.backup_source == "binance":
            return self._fetch_binance(symbol)
        return None

    def _fetch_yahoo(self, symbol):
        """ Fetch price from Yahoo Finance API """
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            latest_price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            return latest_price
        except requests.exceptions.RequestException as e:
            logging.error("Yahoo API Error: %s", e)
            return None

    def _fetch_binance(self, symbol):
        """ Fetch price from Binance API """
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return float(data["price"])
        except requests.exceptions.RequestException as e:
            logging.error("Binance API Error: %s", e)
            return None

    def get_historical_data(self, symbol, period="1y"):
        """
        Fetches historical market data.

        :param symbol: Trading symbol (e.g., "XAUUSD").
        :param period: Period (e.g., "1d", "1w", "1y").
        :return: Pandas DataFrame of historical prices.
        """
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={period}&interval=1d"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            timestamps = data["chart"]["result"][0]["timestamp"]
            closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
            df = pd.DataFrame({"Date": pd.to_datetime(timestamps, unit="s"), "Close": closes})
            logging.info("Fetched historical data for %s (%s)", symbol, period)
            return df
        except requests.exceptions.RequestException as e:
            logging.error("Failed to fetch historical data for %s: %s", symbol, e)
            return None

# Example Usage
if __name__ == "__main__":
    market_data = MarketData()

    # Fetch live price
    live_price = market_data.get_live_price("XAUUSD")
    print("Live Price:", live_price)

    # Fetch historical data
    historical_data = market_data.get_historical_data("XAUUSD", period="1mo")
    print("Historical Data:\n", historical_data)

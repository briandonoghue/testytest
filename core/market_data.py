import logging
import time
import requests
import random
import numpy as np
import pandas as pd
import yfinance as yf


class MarketData:
    """ AI-optimized market data retrieval system """

    def __init__(self, config):
        """
        Initializes the market data handler.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.data_sources = config["settings"]["market_data"].get("data_sources", ["yahoo_finance", "coin_gecko", "binance_public_api"])
        self.fetch_frequency = config["settings"]["market_data"].get("fetch_frequency", "1min")
        self.api_keys = config.get("api_keys", {})

        # Setup logging
        logging.basicConfig(
            filename="logs/market_data.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
    def get_price_change_percentage(self, symbol, period="30d"):
        """
        Calculates the percentage change in price over a given period.
        :param symbol: Trading asset symbol.
        :param period: Time period (e.g., "30d").
        :return: The percentage change in price, or None if unable to calculate.
        """
        historical_data = self.get_historical_data(symbol, period)
        if historical_data and len(historical_data["price"]) > 1:
            initial_price = historical_data["price"][0]  # The first price in the period
            latest_price = historical_data["price"][-1]  # The last price in the period
            price_change_percentage = ((latest_price - initial_price) / initial_price) * 100
            logging.info(f"Price change for {symbol} over {period}: {price_change_percentage:.2f}%")
            return price_change_percentage
        else:
            logging.warning(f"Unable to calculate price change for {symbol} over {period}.")
            return None

    def get_latest_price(self, symbol):
        """
        Retrieves the latest market price using failover data sources.
        :param symbol: Trading asset symbol.
        :return: Latest price or None if unavailable.
        """
        for source in self.data_sources:
            try:
                price = self._fetch_price_from_source(symbol, source)
                if price:
                    logging.info(f"Market data for {symbol} retrieved from {source}: {price}")
                    return price
            except Exception as e:
                logging.warning(f"Failed to fetch market data from {source} for {symbol}: {e}")

        logging.error(f"All data sources failed for {symbol}. Returning None.")
        return None

    def _fetch_price_from_source(self, symbol, source):
        """
        Fetches market data from the specified source.
        :param symbol: Trading asset symbol.
        :param source: Market data provider.
        :return: Latest price or None if unavailable.
        """
        if source == "yahoo_finance":
            return self._fetch_yahoo_finance(symbol)
        elif source == "coin_gecko":
            return self._fetch_coin_gecko(symbol)
        elif source == "binance_public_api":
            return self._fetch_binance(symbol)
        else:
            logging.warning(f"Unknown data source: {source}")
            return None

    def _fetch_yahoo_finance(self, symbol):
        """
        Fetches market data from Yahoo Finance.
        :param symbol: Trading asset symbol.
        :return: Latest price or None if unavailable.
        """
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            return round(price, 2)
        except Exception as e:
            logging.warning(f"Yahoo Finance error: {e}")
            return None

    def _fetch_coin_gecko(self, symbol):
        """
        Fetches market data from CoinGecko API.
        :param symbol: Trading asset symbol.
        :return: Latest price or None if unavailable.
        """
        symbol_mapping = {
            "BTCUSDT": "bitcoin",
            "ETHUSDT": "ethereum"
        }
        coin_id = symbol_mapping.get(symbol, symbol.lower())

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            price = data[coin_id]["usd"]
            return round(price, 2)
        except Exception as e:
            logging.warning(f"CoinGecko error: {e}")
            return None

    def _fetch_binance(self, symbol):
        """
        Fetches market data from Binance public API.
        :param symbol: Trading asset symbol.
        :return: Latest price or None if unavailable.
        """
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            price = float(data["price"])
            return round(price, 2)
        except Exception as e:
            logging.warning(f"Binance API error: {e}")
            return None

    def get_historical_data(self, symbol, period="30d"):
        """
        Retrieves historical market data for AI model training.
        :param symbol: Trading asset symbol.
        :param period: Time period (e.g., "30d", "1y").
        :return: DataFrame containing historical price data or None.
        """
        try:
            # Use Yahoo Finance API to fetch historical data
            data = yf.download(symbol, period=period, interval="1d")
            if data.empty:
                logging.warning(f"No data returned for {symbol} in the period {period}.")
                return None
            
            # Return data as a DataFrame for easier processing
            data = data[['Close']]  # You can modify this to include more columns like Open, High, Low, etc.
            data.reset_index(inplace=True)
            data.rename(columns={"Date": "timestamp", "Close": "price"}, inplace=True)

            # Optional: Convert the data to a dictionary with symbol and price list if needed
            historical_data = {"symbol": symbol, "price": data["price"].tolist(), "timestamp": data["timestamp"].tolist()}
            return historical_data

        except Exception as e:
            logging.error(f"Failed to retrieve historical data for {symbol}: {e}")
            return None

    def get_asset_volatility(self, symbol, period=14):
        """
        Retrieves the asset's volatility over the last 'period' days.
        :param symbol: Trading asset symbol.
        :param period: Number of past days to calculate volatility (default 14 days).
        :return: The calculated volatility (standard deviation of daily returns).
        """
        price_data = self.get_historical_data(symbol, period)
        if price_data is None or len(price_data["price"]) < period:
            return None

        # Calculate daily returns
        daily_returns = np.diff(price_data["price"]) / price_data["price"][:-1]

        # Calculate volatility (standard deviation of daily returns)
        volatility = np.std(daily_returns)
        return round(volatility, 4)  # Rounded for better readability

    def get_market_conditions(self, symbol):
        """
        Retrieves market conditions, including price and volatility.
        :param symbol: Trading asset symbol.
        :return: Dictionary with price and volatility.
        """
        price = self.get_latest_price(symbol)
        volatility = self.get_asset_volatility(symbol)

        if price is None or volatility is None:
            logging.error(f"Failed to fetch market conditions for {symbol}.")
            return None

        return {
            "price": price,
            "volatility": volatility
        }

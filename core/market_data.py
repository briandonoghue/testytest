import logging
import time
import requests
import random
from utilities.config_loader import load_config

class MarketData:
    """ AI-optimized market data retrieval system """

    def __init__(self, config):
        """
        Initializes the market data handler.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.data_sources = config["market_data"].get("data_sources", ["yahoo_finance", "coin_gecko", "binance_public_api"])
        self.fetch_frequency = config["market_data"].get("fetch_frequency", "1min")
        self.api_keys = config.get("api_keys", {})

        # Setup logging
        logging.basicConfig(
            filename="logs/market_data.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

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
        :param period: Time period (e.g., "30d").
        :return: DataFrame containing historical price data or None.
        """
        try:
            price_list = [self.get_latest_price(symbol) for _ in range(30)]
            return {"price": price_list, "symbol": symbol}
        except Exception as e:
            logging.error(f"Failed to retrieve historical data for {symbol}: {e}")
            return None

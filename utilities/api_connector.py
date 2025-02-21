import logging
import os
import requests
import json
from utilities.config_loader import load_config

class APIConnector:
    """ Handles API connections for market data and broker integrations """

    def __init__(self, config):
        """
        Initializes the API connector.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.api_keys = config["api_keys"]
        self.session = requests.Session()

        # Setup logging
        logging.basicConfig(
            filename="logs/api_connector.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def fetch_market_data(self, symbol, provider="yahoo_finance"):
        """
        Retrieves real-time market data from selected API provider.
        :param symbol: Trading asset symbol.
        :param provider: Data provider (yahoo_finance, binance_public_api, coingecko).
        :return: Market price or None if failed.
        """
        provider_urls = {
            "yahoo_finance": f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
            "binance_public_api": f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}",
            "coingecko": f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        }

        if provider not in provider_urls:
            logging.error(f"Market data provider {provider} not supported.")
            return None

        try:
            response = self.session.get(provider_urls[provider], timeout=5)
            if response.status_code == 200:
                data = response.json()
                return self._parse_market_data(data, provider)
            else:
                logging.warning(f"Failed to fetch market data from {provider}: {response.status_code}")
                return None
        except requests.RequestException as e:
            logging.error(f"API request error: {e}")
            return None

    def _parse_market_data(self, data, provider):
        """
        Parses market data from API response.
        :param data: Raw API response data.
        :param provider: Data provider.
        :return: Extracted price or None.
        """
        try:
            if provider == "yahoo_finance":
                return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            elif provider == "binance_public_api":
                return float(data["price"])
            elif provider == "coingecko":
                return list(data.values())[0]["usd"]
        except (KeyError, TypeError):
            logging.error(f"Error parsing market data from {provider}.")
            return None

    def send_order(self, symbol, action, quantity, price, broker="binance"):
        """
        Sends a trade order to the selected broker.
        :param symbol: Trading asset symbol.
        :param action: "buy" or "sell".
        :param quantity: Order quantity.
        :param price: Target execution price.
        :param broker: Broker platform (binance, interactive_brokers).
        :return: Execution confirmation or None.
        """
        broker_urls = {
            "binance": "https://api.binance.com/api/v3/order",
            "interactive_brokers": "https://api.ibkr.com/v1/order"
        }

        if broker not in broker_urls:
            logging.error(f"Broker {broker} not supported.")
            return None

        headers = {"Authorization": f"Bearer {self.api_keys.get(broker.upper(), 'public')}"}
        order_data = {
            "symbol": symbol,
            "side": action.upper(),
            "quantity": quantity,
            "price": price,
            "type": "LIMIT",
            "timeInForce": "GTC"
        }

        try:
            response = self.session.post(broker_urls[broker], json=order_data, headers=headers, timeout=5)
            if response.status_code == 200:
                logging.info(f"Order executed: {response.json()}")
                return response.json()
            else:
                logging.warning(f"Order failed: {response.status_code} - {response.text}")
                return None
        except requests.RequestException as e:
            logging.error(f"API order execution error: {e}")
            return None

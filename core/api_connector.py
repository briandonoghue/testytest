import logging
import requests
import time

class APIConnector:
    """ Handles communication with broker APIs for trade execution """

    def __init__(self, broker_api_url="https://mock-broker.com/api", max_retries=3):
        """
        Initializes API Connector.

        :param broker_api_url: URL for broker's trading API.
        :param max_retries: Maximum retries for failed API requests.
        """
        self.broker_api_url = broker_api_url
        self.max_retries = max_retries

        # Setup logging
        logging.basicConfig(
            filename="logs/api_connector.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def place_order(self, order_data):
        """
        Places a trade order via the broker API.
        
        :param order_data: Dictionary with trade details (symbol, quantity, order type, price).
        :return: API response (success or failure).
        """
        endpoint = f"{self.broker_api_url}/place_order"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(endpoint, json=order_data, timeout=5)
                
                if response.status_code == 200:
                    logging.info("Order placed successfully: %s", response.json())
                    return response.json()
                else:
                    logging.warning("API Error (%d): %s", response.status_code, response.text)
                    
            except requests.exceptions.RequestException as e:
                logging.error("API request failed: %s", e)

            time.sleep(2)  # Wait before retrying
        
        return {"status": "failed", "reason": "API request failed after retries"}

    def get_market_price(self, symbol):
        """
        Retrieves the latest market price for a given asset.
        
        :param symbol: Trading symbol (e.g., "XAUUSD").
        :return: Latest price or None if request fails.
        """
        endpoint = f"{self.broker_api_url}/market_price?symbol={symbol}"

        try:
            response = requests.get(endpoint, timeout=5)

            if response.status_code == 200:
                return response.json().get("price")
            else:
                logging.warning("Failed to get market price: %s", response.text)

        except requests.exceptions.RequestException as e:
            logging.error("Market data request failed: %s", e)

        return None

# Example Usage
if __name__ == "__main__":
    api_connector = APIConnector()

    # Test order placement
    order = {
        "symbol": "XAUUSD",
        "quantity": 1,
        "order_type": "market",
        "price": None
    }
    result = api_connector.place_order(order)
    print("Order Result:", result)

    # Test market price retrieval
    price = api_connector.get_market_price("XAUUSD")
    print("Current Market Price:", price)

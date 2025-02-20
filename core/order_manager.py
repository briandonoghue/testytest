import logging
from api_connector import APIConnector

class OrderManager:
    """ Handles trade execution and order management """

    def __init__(self, api_connector):
        """
        Initializes OrderManager with a broker API connector.
        
        :param api_connector: Instance of APIConnector for trade execution.
        """
        self.api_connector = api_connector

        # Setup logging
        logging.basicConfig(
            filename="logs/order_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def execute_order(self, symbol, quantity, order_type="market", price=None):
        """
        Places a trade order.
        
        :param symbol: Trading symbol (e.g., "XAUUSD").
        :param quantity: Trade size.
        :param order_type: Order type ("market" or "limit").
        :param price: Price for limit orders (optional).
        :return: Order execution result.
        """
        try:
            if quantity <= 0:
                raise ValueError("Trade quantity must be positive.")

            if order_type == "limit" and price is None:
                raise ValueError("Limit orders require a price.")

            order = {
                "symbol": symbol,
                "quantity": quantity,
                "order_type": order_type,
                "price": price
            }

            response = self.api_connector.place_order(order)
            
            if response.get("status") == "filled":
                logging.info("Trade executed: %s, Quantity: %s, Type: %s, Price: %s",
                             symbol, quantity, order_type, price)
            else:
                logging.warning("Trade execution failed: %s", response)

            return response

        except Exception as e:
            logging.error("Trade execution error: %s", e)
            return {"status": "failed", "reason": str(e)}

# Example Usage
if __name__ == "__main__":
    api_connector = APIConnector()
    order_manager = OrderManager(api_connector)

    # Simulate a trade
    result = order_manager.execute_order("XAUUSD", 1, "market")
    print("Trade Result:", result)

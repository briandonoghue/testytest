import logging
import threading

class PortfolioManager:
    def __init__(self, initial_balance=100000):
        """
        Initializes the portfolio manager.

        :param initial_balance: Starting portfolio balance.
        """
        self.cash_balance = initial_balance
        self.holdings = {}  # Format: { "symbol": { "quantity": x, "avg_price": y } }
        self.trade_history = []
        self.lock = threading.Lock()

        # Setup logging
        logging.basicConfig(
            filename="logs/portfolio_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def update_portfolio(self, trade):
        """
        Updates portfolio after a trade execution.

        :param trade: Trade details (dict).
        """
        with self.lock:
            symbol = trade["symbol"]
            quantity = trade["quantity"]
            price = trade["price"]
            trade_type = trade["type"]

            if trade_type == "buy":
                total_cost = price * quantity
                if self.cash_balance >= total_cost:
                    self.cash_balance -= total_cost
                    if symbol in self.holdings:
                        existing_qty = self.holdings[symbol]["quantity"]
                        existing_avg_price = self.holdings[symbol]["avg_price"]
                        new_qty = existing_qty + quantity
                        new_avg_price = ((existing_avg_price * existing_qty) + (price * quantity)) / new_qty
                        self.holdings[symbol] = {"quantity": new_qty, "avg_price": new_avg_price}
                    else:
                        self.holdings[symbol] = {"quantity": quantity, "avg_price": price}

                    self.trade_history.append(trade)
                    logging.info("BUY executed: %s, Qty: %s, Price: %.2f", symbol, quantity, price)
                else:
                    logging.warning("BUY order failed: Insufficient funds for %s", symbol)

            elif trade_type == "sell":
                if symbol in self.holdings and self.holdings[symbol]["quantity"] >= quantity:
                    self.cash_balance += price * quantity
                    self.holdings[symbol]["quantity"] -= quantity
                    if self.holdings[symbol]["quantity"] == 0:
                        del self.holdings[symbol]  # Remove empty holdings

                    self.trade_history.append(trade)
                    logging.info("SELL executed: %s, Qty: %s, Price: %.2f", symbol, quantity, price)
                else:
                    logging.warning("SELL order failed: Not enough holdings for %s", symbol)

    def get_portfolio_value(self, market_data):
        """
        Calculates total portfolio value including holdings.

        :param market_data: Market data provider.
        :return: Total portfolio value.
        """
        total_value = self.cash_balance
        for symbol, position in self.holdings.items():
            market_price = market_data.get_live_price(symbol)
            total_value += market_price * position["quantity"]

        logging.info("Portfolio Value Updated: %.2f", total_value)
        return total_value

    def get_portfolio_summary(self):
        """ Returns a summary of portfolio holdings and balance. """
        return {
            "cash_balance": self.cash_balance,
            "holdings": self.holdings,
            "trade_history": self.trade_history
        }

# Example Usage
if __name__ == "__main__":
    class MockMarketData:
        """ Mock market data provider for testing. """
        def get_live_price(self, symbol):
            return 2100.00  # Example price

    portfolio_manager = PortfolioManager(initial_balance=50000)
    mock_market_data = MockMarketData()

    # Simulate a trade
    trade1 = {"symbol": "XAUUSD", "quantity": 2, "price": 2100.00, "type": "buy"}
    trade2 = {"symbol": "XAUUSD", "quantity": 1, "price": 2110.00, "type": "sell"}

    portfolio_manager.update_portfolio(trade1)
    portfolio_manager.update_portfolio(trade2)

    print("Portfolio Value:", portfolio_manager.get_portfolio_value(mock_market_data))
    print("Portfolio Summary:", portfolio_manager.get_portfolio_summary())

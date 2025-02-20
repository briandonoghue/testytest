import logging
import threading
import time

class StrategyEngine:
    def __init__(self, market_data, order_manager):
        self.market_data = market_data
        self.order_manager = order_manager
        self.active_strategy = None
        self.lock = threading.Lock()

        # Setup logging
        logging.basicConfig(
            filename="logs/strategy_engine.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def load_strategy(self, strategy):
        """ Loads and activates a new trading strategy """
        with self.lock:
            self.active_strategy = strategy
            logging.info("Strategy loaded: %s", strategy.__class__.__name__)

    def evaluate_market(self):
        """ Evaluates market conditions and decides trading actions """
        if not self.active_strategy:
            logging.warning("No strategy loaded. Skipping evaluation.")
            return

        try:
            logging.info("Evaluating market using %s", self.active_strategy.__class__.__name__)
            trade_signal = self.active_strategy.generate_signal(self.market_data)
            if trade_signal:
                self.execute_trade(trade_signal)
        except Exception as e:
            logging.error("Error during market evaluation: %s", e)

    def execute_trade(self, trade_signal):
        """ Executes trade based on strategy signal """
        try:
            order = {
                "symbol": trade_signal["symbol"],
                "quantity": trade_signal["quantity"],
                "price": trade_signal["price"],
                "type": trade_signal["type"]
            }
            self.order_manager.place_order(order)
            logging.info("Trade executed: %s", order)
        except Exception as e:
            logging.error("Trade execution failed: %s", e)

# Example Strategy
class MovingAverageStrategy:
    def generate_signal(self, market_data):
        """ Dummy strategy for generating trade signals """
        latest_price = market_data.get_latest_price("XAUUSD")
        moving_avg = market_data.get_moving_average("XAUUSD", period=50)

        if latest_price > moving_avg:
            return {"symbol": "XAUUSD", "quantity": 1, "price": latest_price, "type": "buy"}
        elif latest_price < moving_avg:
            return {"symbol": "XAUUSD", "quantity": 1, "price": latest_price, "type": "sell"}
        return None

# Example Usage
if __name__ == "__main__":
    class MarketDataMock:
        """ Mock market data source for testing """
        def get_latest_price(self, symbol):
            return 2105.00  # Dummy value

        def get_moving_average(self, symbol, period):
            return 2100.00  # Dummy value

    mock_market_data = MarketDataMock()
    mock_order_manager = OrderManager("https://broker.example.com/orders")
    strategy_engine = StrategyEngine(mock_market_data, mock_order_manager)

    strategy = MovingAverageStrategy()
    strategy_engine.load_strategy(strategy)
    strategy_engine.evaluate_market()

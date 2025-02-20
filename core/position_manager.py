import logging
import threading
import time
from risk_manager import RiskManager
from api_connector import APIConnector

class PositionManager:
    def __init__(self, api_connector, risk_manager, check_interval=5):
        """
        Initializes the Position Manager.

        :param api_connector: Instance of APIConnector.
        :param risk_manager: Instance of RiskManager.
        :param check_interval: Time interval (seconds) for position updates.
        """
        self.api_connector = api_connector
        self.risk_manager = risk_manager
        self.positions = {}  # Stores active positions
        self.check_interval = check_interval
        self.lock = threading.Lock()

        # Setup logging
        logging.basicConfig(
            filename="logs/position_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def add_position(self, symbol, quantity, entry_price, stop_loss=None, take_profit=None):
        """
        Adds a new open position.

        :param symbol: Trading symbol (e.g., "XAUUSD").
        :param quantity: Trade size.
        :param entry_price: Trade entry price.
        :param stop_loss: Stop-loss price (optional).
        :param take_profit: Take-profit price (optional).
        """
        with self.lock:
            if not stop_loss:
                stop_loss = entry_price * (1 - self.risk_manager.stop_loss_pct)

            if not take_profit:
                take_profit = entry_price * (1 + self.risk_manager.take_profit_pct)

            self.positions[symbol] = {
                "quantity": quantity,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit
            }
            logging.info("Position added: %s, Entry: %.2f, SL: %.2f, TP: %.2f",
                         symbol, entry_price, stop_loss, take_profit)

    def monitor_positions(self):
        """ Continuously monitors open positions and triggers stop-loss/take-profit. """
        while True:
            with self.lock:
                for symbol, position in list(self.positions.items()):
                    current_price = self.api_connector.get_market_price(symbol)

                    if current_price is None:
                        continue  # Skip if price is unavailable

                    if current_price <= position["stop_loss"]:
                        logging.warning("Stop-Loss triggered for %s at %.2f", symbol, current_price)
                        self.close_position(symbol, "stop-loss")
                    elif current_price >= position["take_profit"]:
                        logging.info("Take-Profit reached for %s at %.2f", symbol, current_price)
                        self.close_position(symbol, "take-profit")

            time.sleep(self.check_interval)

    def close_position(self, symbol, reason):
        """
        Closes an open position.

        :param symbol: Trading symbol.
        :param reason: Reason for closing (stop-loss, take-profit, manual).
        """
        if symbol not in self.positions:
            logging.error("Attempted to close a non-existent position: %s", symbol)
            return

        position = self.positions.pop(symbol)
        closing_price = self.api_connector.get_market_price(symbol)
        trade_result = self.api_connector.place_order(symbol, position["quantity"], closing_price, "market", "sell")

        logging.info("Position closed: %s, Reason: %s, Closing Price: %.2f",
                     symbol, reason, closing_price)
        return trade_result

# Example Usage
if __name__ == "__main__":
    api_connector = APIConnector(broker="binance")
    risk_manager = RiskManager()

    position_manager = PositionManager(api_connector, risk_manager)

    # Simulate adding a position
    position_manager.add_position(symbol="XAUUSD", quantity=1, entry_price=2100.00)

    # Start monitoring positions
    threading.Thread(target=position_manager.monitor_positions, daemon=True).start()

    # Simulate bot running
    time.sleep(20)

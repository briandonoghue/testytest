# execution_engine.py
from logger import setup_logging  # Importing logger for debugging
import threading

# Delayed Import to Prevent Circular Import Issues
def get_order_manager():
    from core.order_manager import OrderManager
    return OrderManager

class ExecutionEngine:
    def __init__(self):
        self.logger = setup_logging()
        self.order_manager = None  # Initialized later to avoid circular dependency
    
    def initialize(self):
        """Initialize dependencies."""
        self.order_manager = get_order_manager()()  # Instantiate OrderManager without circular imports
        self.logger.info("ExecutionEngine initialized successfully.")

    def execute_trade(self, trade_order):
        """Execute trade using order manager."""
        if not self.order_manager:
            self.initialize()  # Ensure order manager is initialized
        
        self.logger.info(f"Executing trade: {trade_order}")
        return self.order_manager.process_order(trade_order)
        """
        Process trade signals and execute orders.
        :param trade_signal: dict containing trade details (symbol, action, quantity, etc.)
        """
        try:
            symbol = trade_signal.get("symbol")
            action = trade_signal.get("action")
            quantity = trade_signal.get("quantity")

            if not symbol or not action or quantity is None:
                self.logger.error("Invalid trade signal received: %s", trade_signal)
                return False

            self.logger.info("Processing trade signal: %s", trade_signal)
            
            # Validate and place order
            order_id = self.order_manager.place_order(symbol, action, quantity)
            if order_id:
                execution_status = self.trade_executor.execute_order(order_id)
                if execution_status:
                    self.logger.info("Trade executed successfully: %s", trade_signal)
                    return True
                else:
                    self.logger.error("Trade execution failed for order: %s", order_id)
            else:
                self.logger.error("Order placement failed for trade signal: %s", trade_signal)
        
        except Exception as e:
            self.logger.exception("Error executing trade: %s", str(e))
            return False

    def cancel_trade(self, order_id):
        """
        Cancel an existing order.
        :param order_id: ID of the order to cancel.
        """
        try:
            self.logger.info("Attempting to cancel order: %s", order_id)
            success = self.order_manager.cancel_order(order_id)
            if success:
                self.logger.info("Order %s cancelled successfully.", order_id)
                return True
            else:
                self.logger.error("Failed to cancel order %s.", order_id)
                return False
        except Exception as e:
            self.logger.exception("Error cancelling order: %s", str(e))
            return False

"""
Core package: Handles main trading logic, strategy execution, and risk management.
"""

import logging

# Setup logging for core module
logging.basicConfig(
    filename="logs/core.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Explicitly list available modules
__all__ = [
    "main",  # Main entry point for bot execution
    "config_loader",  # Configuration loader (loads settings, API keys, and other preferences)
    "order_manager",  # Manages orders, sending buy/sell signals to the broker
    "strategy_engine",  # Core strategy logic and optimization engine
    "risk_manager",  # Risk management strategies and position sizing
    "backtester",  # Backtesting module to test strategies using historical data
    "market_data",  # Module for fetching market data (real-time and historical)
    "trade_executor",  # Executes trades on the selected platform (e.g., IBKR)
    "portfolio_manager",  # Manages the portfolio, including asset allocation and rebalancing
    "data_analyzer",  # Analyzes the market data and trading signals
    "trade_logger",  # Logs trades executed by the bot
    "notification_manager",  # Sends notifications based on alerts (email, SMS, etc.)
    "alert_manager",  # Handles setting up and triggering alerts based on market conditions
    "error_handler",  # Error handling and logging
    "report_generator",  # Generates reports and analytics of bot's performance
    "performance_tracker",  # Tracks and visualizes bot's performance over time
    "api_connector",  # Handles API connections to external brokers and services
    "position_manager"  # Manages positions, open/close orders, and stop-loss strategies
]

# Additional initialization steps (if necessary)
def initialize_core_components():
    """
    Initialize core components like risk management, order management, etc.
    This function can be used to ensure all modules are properly configured
    before the bot starts trading.
    """
    logging.info("Initializing core components...")
    # Here, you can initialize key components like the risk manager, order manager, etc.
    # Example:
    # risk_manager.init()
    # order_manager.init()
    # This can be expanded as needed depending on the structure of each module.

    logging.info("Core components initialized successfully.")

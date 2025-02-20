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
    "main",
    "config_loader",
    "order_manager",
    "strategy_engine",
    "risk_manager",
    "backtester",
    "market_data",
    "trade_executor",
    "portfolio_manager",
    "data_analyzer",
    "trade_logger",
    "notification_manager",
    "alert_manager",
    "error_handler",
    "report_generator",
    "performance_tracker",
    "api_connector",
    "position_manager"
]

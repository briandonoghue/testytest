"""
Core module initialization for TradingBot.

This module includes the execution engine, order management, data handling,
and trading logic required for automated trading.
"""

# Importing key components
from execution_engine import ExecutionEngine
from order_manager import OrderManager
from trade_executor import TradeExecutor
from config_loader import ConfigLoader
from logger import Logger

# Define what should be available when using `from core import *`
__all__ = [
    "ExecutionEngine",
    "OrderManager",
    "TradeExecutor",
    "ConfigLoader",
    "Logger",
]

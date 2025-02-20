"""
Tests package: Contains unit tests for all major components.
"""

import logging

logging.basicConfig(
    filename="logs/tests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Explicitly list available test modules
__all__ = [
    "test_order_manager",
    "test_risk_manager",
    "test_market_data",
    "test_trade_executor",
    "test_sentiment_analyzer",
    "test_hyperparameter_tuner"
]

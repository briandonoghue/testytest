"""
Strategies package: Contains different trading strategy implementations.
"""

import logging

logging.basicConfig(
    filename="logs/strategies.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Explicitly list available strategy modules
__all__ = [
    "moving_average",
    "rsi_strategy",
    "volatility_breakout"
]

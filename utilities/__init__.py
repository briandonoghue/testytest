"""
Utilities package: Contains helper functions for math, config, and time management.
"""

import logging

logging.basicConfig(
    filename="logs/utilities.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Explicitly list available utility modules
__all__ = [
    "config_utils",
    "math_utils",
    "time_utils"
]

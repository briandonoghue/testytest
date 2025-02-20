"""
Dashboard package: Provides UI components for monitoring trading performance.
"""

import logging

logging.basicConfig(
    filename="logs/dashboard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Explicitly list available modules
__all__ = [
    "dashboard",
    "ui_components",
    "error_display"
]

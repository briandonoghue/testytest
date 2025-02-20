"""
Machine Learning (ML) package: Handles AI-powered strategy optimization and training.
"""

import logging

logging.basicConfig(
    filename="logs/ml.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Explicitly list available modules
__all__ = [
    "ai_strategy_optimizer",
    "model_training",
    "data_preprocessor",
    "drl_trader",
    "sentiment_analyzer",
    "ai_trainer",
    "hyperparameter_tuner"
]

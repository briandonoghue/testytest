import unittest
import json
import numpy as np
from ml.reinforcement_learning import ReinforcementLearningAI
from ml.ai_execution_optimizer import AIExecutionOptimizer

class TestMLModel(unittest.TestCase):
    """ Unit tests for AI-powered machine learning models """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize AI models """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.rl_model = ReinforcementLearningAI(cls.config)
        cls.execution_optimizer = AIExecutionOptimizer(cls.config)

    def test_rl_model_training(self):
        """ Ensure AI reinforcement learning model trains correctly """
        symbol = "BTCUSDT"
        initial_epsilon = cls.rl_model.epsilon

        cls.rl_model.train_rl_model(symbol)
        
        self.assertLess(cls.rl_model.epsilon, initial_epsilon, "Epsilon should decrease after training")
        self.assertGreater(cls.rl_model.memory.maxlen, 1000, "Training memory should store sufficient samples")

    def test_trade_prediction(self):
        """ Validate AI predicts optimal trade action correctly """
        symbol = "ETHUSDT"
        prediction = cls.rl_model.predict_trade_action(symbol)

        self.assertIsInstance(prediction, dict, "Prediction should return a dictionary")
        self.assertIn(prediction["action"], ["Hold", "Buy", "Sell"], "Predicted action should be valid")
        self.assertGreaterEqual(prediction["confidence"], 0, "Confidence should be non-negative")
        self.assertLessEqual(prediction["confidence"], 1, "Confidence should be normalized")

    def test_execution_optimization(self):
        """ Ensure AI execution optimizer improves trade timing """
        symbol = "XAUUSD"
        execution_data = cls.execution_optimizer.analyze_execution_conditions(symbol)

        self.assertIsInstance(execution_data, dict, "Execution data should return a dictionary")
        self.assertIn(execution_data["preferred_order_type"], ["LIMIT", "MARKET"], "Order type should be valid")
        self.assertGreaterEqual(execution_data["execution_delay"], 0, "Execution delay should be non-negative")

    def test_slippage_control(self):
        """ Validate AI optimizes slippage during trade execution """
        trade_signal = {"symbol": "BTCUSDT", "price": 50000}
        adjusted_execution = cls.execution_optimizer.optimize_slippage_control(trade_signal)

        self.assertIsInstance(adjusted_execution, dict, "Slippage control should return a dictionary")
        self.assertGreater(adjusted_execution["adjusted_price"], 0, "Adjusted price should be positive")
        self.assertLessEqual(abs(adjusted_execution["adjusted_price"] - trade_signal["price"]), trade_signal["price"] * cls.execution_optimizer.slippage_tolerance, "Slippage should be within AI-defined tolerance")

if __name__ == "__main__":
    unittest.main()

import unittest
import json
import numpy as np
from ml.self_training import MLSelfTrainer

class TestMLSelfTraining(unittest.TestCase):
    """ Unit tests for AI-powered self-learning and model retraining """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize MLSelfTrainer """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.ml_trainer = MLSelfTrainer(cls.config)

    def test_data_preprocessing(self):
        """ Ensure AI correctly preprocesses market data for training """
        raw_data = np.array([
            [50000, 1.5, 0.02],  # [price, volume, volatility]
            [50500, 1.3, 0.015],
            [49500, 1.6, 0.03]
        ])

        processed_data = self.ml_trainer.preprocess_data(raw_data)

        self.assertIsInstance(processed_data, np.ndarray, "Processed data should be a NumPy array")
        self.assertEqual(processed_data.shape[1], 3, "Processed data should have correct features")

    def test_model_training(self):
        """ Validate AI correctly trains and updates models """
        training_data = np.random.rand(100, 3)  # 100 samples, 3 features
        training_labels = np.random.choice([0, 1], size=100)  # 0 = no trade, 1 = trade

        training_result = self.ml_trainer.train_model(training_data, training_labels)

        self.assertTrue(training_result, "AI model should successfully train on new data")

    def test_live_model_update(self):
        """ Ensure AI updates its model dynamically based on real-time market performance """
        new_market_data = np.random.rand(10, 3)  # 10 new market samples

        update_result = self.ml_trainer.update_model(new_market_data)

        self.assertTrue(update_result, "AI should successfully update its model with new market data")

    def test_feature_selection_optimization(self):
        """ Validate AI selects the most important trading features dynamically """
        initial_features = ["SMA_50", "SMA_200", "RSI", "MACD", "Order Flow", "Momentum"]

        optimized_features = self.ml_trainer.optimize_feature_selection(initial_features)

        self.assertIsInstance(optimized_features, list, "Optimized features should be returned as a list")
        self.assertLessEqual(len(optimized_features), len(initial_features), "Feature selection should reduce less important features")

    def test_retraining_trigger_conditions(self):
        """ Ensure AI retrains itself only when performance metrics demand it """
        performance_metrics = {
            "win_rate": 48.0,  # Below optimal threshold
            "sharpe_ratio": 0.9,
            "max_drawdown": 6.5
        }

        retrain_needed = self.ml_trainer.check_retraining_need(performance_metrics)

        self.assertTrue(retrain_needed, "AI should trigger retraining if performance drops below threshold")

    def test_training_log_integration(self):
        """ Ensure AI logs retraining cycles for tracking and improvements """
        retraining_log = {
            "timestamp": "2025-02-20 21:30:00",
            "new_features_used": ["SMA_50", "RSI", "Order Flow"],
            "performance_improvement": 5.2
        }

        log_result = self.ml_trainer.log_retraining(retraining_log)

        self.assertTrue(log_result, "AI should successfully log retraining events")

if __name__ == "__main__":
    unittest.main()

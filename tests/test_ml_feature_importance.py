import unittest
import json
import numpy as np
from ml.feature_importance import MLFeatureImportance

class TestMLFeatureImportance(unittest.TestCase):
    """ Unit tests for AI-powered feature selection and importance ranking """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize MLFeatureImportance """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.feature_importance = MLFeatureImportance(cls.config)

    def test_calculate_feature_importance(self):
        """ Ensure AI correctly ranks trading features by importance """
        feature_data = np.random.rand(100, 5)  # 100 samples, 5 features
        labels = np.random.choice([0, 1], size=100)  # 0 = no trade, 1 = trade

        ranked_features = self.feature_importance.calculate_importance(feature_data, labels)

        self.assertIsInstance(ranked_features, dict, "Feature importance ranking should return a dictionary")
        self.assertGreaterEqual(len(ranked_features), 3, "AI should prioritize at least 3 key features")

    def test_dynamic_feature_selection(self):
        """ Validate AI dynamically selects the best features for model training """
        initial_features = ["SMA_50", "SMA_200", "RSI", "MACD", "Momentum", "Volume", "VWAP"]

        optimized_features = self.feature_importance.optimize_feature_selection(initial_features)

        self.assertIsInstance(optimized_features, list, "Optimized features should be a list")
        self.assertLessEqual(len(optimized_features), len(initial_features), "Feature selection should remove less relevant features")
        self.assertIn("RSI", optimized_features, "Commonly used features like RSI should remain if relevant")

    def test_feature_removal_for_overfitting(self):
        """ Ensure AI removes features that cause overfitting """
        overfit_features = {
            "SMA_20": 0.02,  # Low importance score
            "MACD": 0.45,
            "Order Flow": 0.03,  # Low importance
            "Momentum": 0.5
        }

        reduced_feature_set = self.feature_importance.remove_overfit_features(overfit_features)

        self.assertIsInstance(reduced_feature_set, dict, "Reduced feature set should be a dictionary")
        self.assertNotIn("SMA_20", reduced_feature_set, "Low-impact features should be removed")
        self.assertNotIn("Order Flow", reduced_feature_set, "Overfit features should be discarded")

    def test_market_condition_adaptive_feature_selection(self):
        """ Validate AI adapts feature selection based on market conditions """
        market_conditions = {
            "volatility": 0.05,
            "trend_strength": 0.8,
            "liquidity": 0.6
        }

        selected_features = self.feature_importance.adapt_features_to_market(market_conditions)

        self.assertIsInstance(selected_features, list, "Market-adaptive feature selection should return a list")
        self.assertGreaterEqual(len(selected_features), 3, "AI should use at least 3 core features")
        self.assertIn("Momentum", selected_features, "Momentum should be included during strong trends")

    def test_feature_importance_log_integration(self):
        """ Ensure AI logs feature importance rankings for strategy review """
        feature_log_entry = {
            "timestamp": "2025-02-20 22:30:00",
            "top_features": ["RSI", "Momentum", "VWAP"],
            "dropped_features": ["SMA_20", "Order Flow"]
        }

        log_result = self.feature_importance.log_feature_importance(feature_log_entry)

        self.assertTrue(log_result, "AI should successfully log feature importance rankings")

if __name__ == "__main__":
    unittest.main()

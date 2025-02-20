import unittest
from unittest.mock import patch
from ml.hyperparameter_tuner import HyperparameterTuner

class TestHyperparameterTuner(unittest.TestCase):
    """ Unit tests for AI Hyperparameter Tuning """

    def setUp(self):
        """ Initializes HyperparameterTuner instance. """
        self.tuner = HyperparameterTuner()

    @patch("ml.hyperparameter_tuner.DQN")
    @patch("ml.hyperparameter_tuner.DummyVecEnv")
    def test_tune_hyperparameters(self, mock_env, mock_dqn):
        """ Tests hyperparameter tuning process and selects best model. """
        # Mock AI model training process
        mock_model_instance = mock_dqn.return_value
        mock_model_instance.learn.return_value = None  # Simulating model training
        mock_model_instance.save.return_value = None

        # Mock backtest performance results
        self.tuner.backtester.run_backtest = lambda: {"Total Profit": 5000}

        best_params = self.tuner.tune_hyperparameters()
        
        self.assertIn("learning_rate", best_params)
        self.assertIn("batch_size", best_params)
        self.assertIn("gamma", best_params)
        self.assertGreater(best_params["learning_rate"], 0)
        self.assertGreater(best_params["batch_size"], 0)

    def test_default_hyperparameters(self):
        """ Ensures default hyperparameter grid is correctly defined. """
        self.assertIsInstance(self.tuner.tune_hyperparameters(), dict)

    @patch("ml.hyperparameter_tuner.DQN")
    def test_invalid_hyperparameter_values(self, mock_dqn):
        """ Ensures AI does not train with invalid hyperparameter values. """
        self.tuner.learning_rates = [-0.001, 0]  # Invalid learning rates
        self.tuner.batch_sizes = [-32, 0]  # Invalid batch sizes

        best_params = self.tuner.tune_hyperparameters()
        
        self.assertEqual(best_params, {})  # Expecting no valid hyperparameter selection

if __name__ == "__main__":
    unittest.main()

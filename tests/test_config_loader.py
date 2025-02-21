import unittest
import json
import os
from utilities.config_loader import load_config, save_config

class TestConfigLoader(unittest.TestCase):
    """ Unit tests for AI-driven configuration handling """

    @classmethod
    def setUpClass(cls):
        """ Create a test config file """
        cls.test_config_path = "config/test_config.json"
        cls.sample_config = {
            "trading_settings": {
                "cycle_interval": 5,
                "max_trades_per_cycle": 3,
                "trade_execution_type": "market"
            },
            "risk_management": {
                "max_drawdown": 5.0,
                "stop_loss_buffer": 0.02,
                "take_profit_buffer": 0.04
            },
            "api_keys": {
                "BINANCE_API_KEY": "public",
                "BINANCE_API_SECRET": "public"
            }
        }

        with open(cls.test_config_path, "w") as f:
            json.dump(cls.sample_config, f, indent=4)

    @classmethod
    def tearDownClass(cls):
        """ Remove the test config file after tests complete """
        if os.path.exists(cls.test_config_path):
            os.remove(cls.test_config_path)

    def test_load_valid_config(self):
        """ Ensure AI correctly loads a valid configuration file """
        config = load_config(self.test_config_path)

        self.assertIsInstance(config, dict, "Configuration should be loaded as a dictionary")
        self.assertIn("trading_settings", config, "Configuration should include trading settings")
        self.assertEqual(config["trading_settings"]["cycle_interval"], 5, "Cycle interval should be correctly loaded")

    def test_handle_missing_config(self):
        """ Ensure AI correctly handles a missing configuration file """
        missing_path = "config/missing_config.json"
        config = load_config(missing_path)

        self.assertIsNone(config, "AI should return None for missing configuration files")

    def test_handle_corrupted_config(self):
        """ Ensure AI correctly handles corrupted configuration files """
        corrupted_path = "config/corrupted_config.json"

        with open(corrupted_path, "w") as f:
            f.write("{invalid_json:}")  # Writing corrupted JSON

        config = load_config(corrupted_path)
        self.assertIsNone(config, "AI should return None for corrupted configuration files")

        # Clean up
        os.remove(corrupted_path)

    def test_save_config_updates_correctly(self):
        """ Validate AI correctly updates and saves configuration settings """
        new_config = self.sample_config
        new_config["trading_settings"]["cycle_interval"] = 10

        save_config(self.test_config_path, new_config)
        updated_config = load_config(self.test_config_path)

        self.assertEqual(updated_config["trading_settings"]["cycle_interval"], 10, "Cycle interval should be updated correctly")

if __name__ == "__main__":
    unittest.main()

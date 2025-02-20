import importlib
import os
import json
from config_loader import ConfigLoader
import logging

class StrategyManager:
    def __init__(self, strategy_config="strategies.json"):
        """
        Manages trading strategies dynamically.
        :param strategy_config: Path to the strategy configuration file.
        """
        self.logger = logging.Logger("StrategyManager")
        self.strategy_config = strategy_config
        self.strategies = self._load_strategies()

    def _load_strategies(self):
        """
        Loads trading strategies from a JSON configuration file.
        :return: Dictionary of strategy configurations.
        """
        if not os.path.exists(self.strategy_config):
            self.logger.error(f"Strategy configuration file not found: {self.strategy_config}")
            return {}

        try:
            with open(self.strategy_config, "r") as file:
                strategies = json.load(file)
                self.logger.info(f"Strategies loaded from {self.strategy_config}")
                return strategies
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing strategy file: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error loading strategies: {e}")
            return {}

    def get_strategy(self, strategy_name):
        """
        Retrieves a specific strategy configuration.
        :param strategy_name: The name of the strategy.
        :return: The strategy configuration or None if not found.
        """
        return self.strategies.get(strategy_name, None)

    def load_strategy_class(self, strategy_name):
        """
        Dynamically loads and returns a strategy class.
        :param strategy_name: The strategy to load.
        :return: Strategy class instance if found, otherwise None.
        """
        strategy_info = self.get_strategy(strategy_name)
        if not strategy_info:
            self.logger.error(f"Strategy '{strategy_name}' not found in configuration.")
            return None

        module_path = strategy_info.get("module")
        class_name = strategy_info.get("class")

        try:
            strategy_module = importlib.import_module(module_path)
            strategy_class = getattr(strategy_module, class_name)
            self.logger.info(f"Successfully loaded strategy: {strategy_name}")
            return strategy_class()
        except ModuleNotFoundError:
            self.logger.error(f"Module '{module_path}' not found.")
        except AttributeError:
            self.logger.error(f"Class '{class_name}' not found in module '{module_path}'.")
        except Exception as e:
            self.logger.error(f"Unexpected error loading strategy '{strategy_name}': {e}")

        return None

    def list_strategies(self):
        """
        Lists all available strategies.
        :return: List of strategy names.
        """
        return list(self.strategies.keys())

if __name__ == "__main__":
    strategy_manager = StrategyManager("strategies.json")
    print("Available Strategies:", strategy_manager.list_strategies())

    strategy_instance = strategy_manager.load_strategy_class("momentum")
    if strategy_instance:
        print(f"Loaded strategy: {strategy_instance.__class__.__name__}")

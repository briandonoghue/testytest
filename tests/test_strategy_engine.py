import unittest
import json
from core.strategy_engine import StrategyEngine
from core.market_data import MarketData

class TestStrategyEngine(unittest.TestCase):
    """ Unit tests for AI-powered trading strategy engine """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize StrategyEngine """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.strategy_engine = StrategyEngine(cls.config)
        cls.market_data = MarketData(cls.config)

    def test_strategy_signal_generation(self):
        """ Ensure AI correctly generates trade signals based on market conditions """
        trade_signal = self.strategy_engine.generate_trade_signal("BTCUSDT")

        self.assertIsNotNone(trade_signal, "Trade signal generation failed")
        self.assertIn(trade_signal["action"], ["BUY", "SELL", "HOLD"], "Invalid trade action")

    def test_ai_strategy_switching(self):
        """ Validate AI correctly switches strategies based on market conditions """
        initial_strategy = self.strategy_engine.current_strategy
        self.strategy_engine.evaluate_market_conditions("BTCUSDT")

        new_strategy = self.strategy_engine.current_strategy
        self.assertNotEqual(initial_strategy, new_strategy, "AI strategy should switch based on market conditions")

    def test_strategy_risk_adjustment(self):
        """ Ensure AI adjusts strategy risk dynamically """
        market_conditions = {"volatility": 0.05, "liquidity": 0.7}
        adjusted_strategy = self.strategy_engine.adjust_strategy_risk("BTCUSDT", market_conditions)

        self.assertIsNotNone(adjusted_strategy, "Strategy risk adjustment failed")
        self.assertIn("risk_level", adjusted_strategy, "Adjusted strategy should include risk level")

    def test_historical_backtest_validation(self):
        """ Validate AI trading strategy logic using historical data """
        test_asset = "ETHUSDT"
        trade_signals = self.strategy_engine.backtest_strategy(test_asset, period="90d")

        self.assertIsInstance(trade_signals, list, "Backtest should return a list of trade signals")
        self.assertGreaterEqual(len(trade_signals), 10, "Backtest should generate sufficient signals for validation")

    def test_ai_profitability_prediction(self):
        """ Ensure AI predicts profitability correctly based on strategy performance """
        test_asset = "XAUUSD"
        prediction = self.strategy_engine.predict_strategy_profitability(test_asset)

        self.assertIsNotNone(prediction, "Profitability prediction failed")
        self.assertGreaterEqual(prediction["expected_profit"], 0, "AI should not predict negative profitability by default")

if __name__ == "__main__":
    unittest.main()

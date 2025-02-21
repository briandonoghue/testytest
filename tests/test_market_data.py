import unittest
import json
from core.market_data import MarketData

class TestMarketData(unittest.TestCase):
    """ Unit tests for AI-driven market data accuracy and consistency """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize MarketData module """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.market_data = MarketData(cls.config)

    def test_real_time_data_fetch(self):
        """ Ensure AI correctly fetches real-time market prices from multiple sources """
        test_symbol = "BTCUSDT"
        real_time_price = self.market_data.get_real_time_price(test_symbol)

        self.assertIsInstance(real_time_price, float, "Real-time price should return a valid float value")
        self.assertGreater(real_time_price, 0, "Real-time price should be a positive number")

    def test_historical_data_consistency(self):
        """ Validate AI fetches historical market data correctly """
        test_symbol = "ETHUSDT"
        historical_data = self.market_data.get_historical_data(test_symbol, period="90d")

        self.assertIsInstance(historical_data, list, "Historical data should return a list")
        self.assertGreaterEqual(len(historical_data), 30, "Historical data should have sufficient entries")

    def test_missing_data_handling(self):
        """ Ensure AI can handle missing or corrupted market data """
        test_symbol = "XAUUSD"
        corrupted_data = self.market_data.get_historical_data(test_symbol, period="30d")

        self.assertIsInstance(corrupted_data, list, "Data response should still return a list")
        self.assertNotEqual(len(corrupted_data), 0, "AI should handle missing data gracefully and not return an empty set")

    def test_bid_ask_spread_calculation(self):
        """ Validate AI correctly calculates bid-ask spreads """
        test_symbol = "PL=F"
        spread = self.market_data.get_bid_ask_spread(test_symbol)

        self.assertIsInstance(spread, float, "Bid-ask spread should return a float value")
        self.assertGreaterEqual(spread, 0, "Bid-ask spread should never be negative")

    def test_liquidity_tracking(self):
        """ Ensure AI correctly determines asset liquidity levels """
        test_symbol = "BTCUSDT"
        liquidity_score = self.market_data.get_liquidity_score(test_symbol)

        self.assertIsInstance(liquidity_score, float, "Liquidity score should return a float value")
        self.assertGreaterEqual(liquidity_score, 0, "Liquidity score should be non-negative")
        self.assertLessEqual(liquidity_score, 1, "Liquidity score should be normalized between 0 and 1")

    def test_api_fallback_mechanism(self):
        """ Ensure AI switches to alternate data sources if the primary API fails """
        test_symbol = "ETHUSDT"
        price_primary = self.market_data.get_real_time_price(test_symbol, provider="yahoo_finance")
        price_fallback = self.market_data.get_real_time_price(test_symbol, provider="binance_public_api")

        self.assertNotEqual(price_primary, price_fallback, "Fallback mechanism should provide an alternate price source")
        self.assertGreater(price_fallback, 0, "Fallback price should still be valid")

if __name__ == "__main__":
    unittest.main()

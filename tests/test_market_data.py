import unittest
from unittest.mock import patch
from core.market_data import MarketData

class TestMarketData(unittest.TestCase):
    def setUp(self):
        """ Initializes MarketData with a mock API. """
        self.market_data = MarketData(primary_source="yahoo")

    @patch("core.market_data.requests.get")
    def test_get_live_price_success(self, mock_get):
        """ Tests successful live price retrieval. """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "chart": {"result": [{"meta": {"regularMarketPrice": 2105.50}}]}
        }

        price = self.market_data.get_live_price("XAUUSD")
        self.assertAlmostEqual(price, 2105.50, places=2)

    @patch("core.market_data.requests.get")
    def test_get_live_price_failure(self, mock_get):
        """ Tests handling of API failure. """
        mock_get.side_effect = Exception("API Down")

        price = self.market_data.get_live_price("XAUUSD")
        self.assertIsNone(price)

    @patch("core.market_data.requests.get")
    def test_get_historical_data_success(self, mock_get):
        """ Tests historical data retrieval. """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "chart": {
                "result": [{
                    "timestamp": [1620000000, 1620086400],
                    "indicators": {"quote": [{"close": [2100.00, 2110.50]}]}
                }]
            }
        }

        data = self.market_data.get_historical_data("XAUUSD", "1mo")
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)

    @patch("core.market_data.requests.get")
    def test_get_historical_data_failure(self, mock_get):
        """ Tests handling of historical data API failure. """
        mock_get.side_effect = Exception("API Timeout")

        data = self.market_data.get_historical_data("XAUUSD", "1mo")
        self.assertIsNone(data)

if __name__ == "__main__":
    unittest.main()

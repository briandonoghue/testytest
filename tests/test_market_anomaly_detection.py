import unittest
import json
from core.market_anomaly_detection import MarketAnomalyDetector

class TestMarketAnomalyDetection(unittest.TestCase):
    """ Unit tests for AI-powered market anomaly detection """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize MarketAnomalyDetector """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.anomaly_detector = MarketAnomalyDetector(cls.config)

    def test_detect_flash_crash(self):
        """ Ensure AI correctly detects flash crashes """
        market_data = {
            "BTCUSDT": {"price_change": -15.0, "volume_spike": 3.2, "bid_ask_spread": 0.05}
        }

        anomaly_detected = self.anomaly_detector.detect_flash_crash("BTCUSDT", market_data)

        self.assertTrue(anomaly_detected, "AI should detect a flash crash in extreme price drops")

    def test_detect_liquidity_trap(self):
        """ Validate AI identifies liquidity traps correctly """
        market_data = {
            "ETHUSDT": {"order_book_imbalance": 0.9, "sudden_spread_widening": 0.07}
        }

        liquidity_trap_detected = self.anomaly_detector.detect_liquidity_trap("ETHUSDT", market_data)

        self.assertTrue(liquidity_trap_detected, "AI should detect a liquidity trap in highly imbalanced order books")

    def test_volatility_spike_detection(self):
        """ Ensure AI flags unexpected volatility spikes """
        market_data = {
            "XAUUSD": {"volatility": 0.12, "historical_volatility": 0.03}
        }

        volatility_spike = self.anomaly_detector.detect_volatility_spike("XAUUSD", market_data)

        self.assertTrue(volatility_spike, "AI should flag excessive volatility increases")

    def test_order_book_manipulation_detection(self):
        """ Validate AI detects spoofing and order book manipulation """
        order_book_data = {
            "PL=F": {"fake_bid_orders": 0.85, "order_cancellation_rate": 0.78}
        }

        manipulation_detected = self.anomaly_detector.detect_order_book_manipulation("PL=F", order_book_data)

        self.assertTrue(manipulation_detected, "AI should detect high fake bid order presence")

    def test_anomaly_log_integration(self):
        """ Ensure AI logs detected anomalies for risk assessment """
        anomaly_event = {
            "symbol": "BTCUSDT",
            "anomaly_type": "Flash Crash",
            "severity": "HIGH",
            "timestamp": "2025-02-20 19:30:00"
        }

        log_result = self.anomaly_detector.log_anomaly_detection(anomaly_event)

        self.assertTrue(log_result, "AI should successfully log anomaly detection events")

if __name__ == "__main__":
    unittest.main()

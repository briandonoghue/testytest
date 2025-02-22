import logging
import numpy as np
from market_data import MarketData
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

class MarketAnomalyDetector:
    """Detects market anomalies based on historical data and advanced statistical techniques"""

    def __init__(self, config):
        """
        Initializes the anomaly detection system.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.scaler = StandardScaler()

        # Setup logging
        logging.basicConfig(
            filename="logs/market_anomaly_detector.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def detect_anomaly(self, symbol):
        """
        Detects market anomalies for the specified trading asset.
        :param symbol: Trading asset symbol.
        :return: Boolean indicating if an anomaly was detected.
        """
        # Fetch historical market data
        market_data = self.market_data.get_historical_data(symbol, period="180d")  # last 6 months
        if market_data is None:
            logging.warning(f"No market data available for {symbol}.")
            return False

        # Preprocess data
        features = self._extract_features(market_data)
        if features is None:
            logging.warning(f"Unable to extract features for {symbol}. Skipping anomaly detection.")
            return False

        # Standardize features
        features_scaled = self.scaler.fit_transform(features)

        # Use the trained Isolation Forest model to detect anomalies
        anomaly_predictions = self.model.fit_predict(features_scaled)

        # If the prediction is -1, it's an anomaly (outlier)
        anomaly_detected = -1 in anomaly_predictions

        if anomaly_detected:
            logging.warning(f"Market anomaly detected for {symbol}.")
        else:
            logging.info(f"No anomalies detected for {symbol}.")

        return anomaly_detected

    def _extract_features(self, market_data):
        """
        Extracts relevant features from market data to be used for anomaly detection.
        :param market_data: Historical market data.
        :return: Numpy array containing the extracted features.
        """
        try:
            # Calculate price change percentage
            market_data['price_change'] = market_data['price'].pct_change()

            # Calculate moving averages
            market_data['SMA_50'] = market_data['price'].rolling(window=50).mean()
            market_data['SMA_200'] = market_data['price'].rolling(window=200).mean()

            # Calculate volatility (standard deviation)
            market_data['volatility'] = market_data['price'].rolling(window=20).std()

            # Drop missing values caused by rolling calculations
            market_data = market_data.dropna()

            # Extract features: Price change, moving averages, and volatility
            features = market_data[['price_change', 'SMA_50', 'SMA_200', 'volatility']].values

            return features
        except Exception as e:
            logging.error(f"Error while extracting features for anomaly detection: {e}")
            return None


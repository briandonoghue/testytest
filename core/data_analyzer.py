import logging
import pandas as pd

class DataAnalyzer:
    def __init__(self):
        """
        Initializes the DataAnalyzer for processing historical market data.
        """
        # Setup logging
        logging.basicConfig(
            filename="logs/data_analyzer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def calculate_moving_average(self, data, period=50):
        """
        Calculates the moving average for a given period.

        :param data: Pandas DataFrame with "Close" prices.
        :param period: Lookback period for moving average.
        :return: Pandas Series with moving average values.
        """
        if "Close" not in data.columns:
            logging.error("Missing 'Close' column in data.")
            return None

        ma = data["Close"].rolling(window=period).mean()
        logging.info("Calculated %d-day moving average", period)
        return ma

    def calculate_rsi(self, data, period=14):
        """
        Calculates the Relative Strength Index (RSI).

        :param data: Pandas DataFrame with "Close" prices.
        :param period: Lookback period for RSI calculation.
        :return: Pandas Series with RSI values.
        """
        if "Close" not in data.columns:
            logging.error("Missing 'Close' column in data.")
            return None

        delta = data["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        logging.info("Calculated %d-day RSI", period)
        return rsi

    def calculate_bollinger_bands(self, data, period=20, std_dev=2):
        """
        Calculates Bollinger Bands.

        :param data: Pandas DataFrame with "Close" prices.
        :param period: Moving average period.
        :param std_dev: Standard deviation multiplier.
        :return: DataFrame with upper and lower Bollinger Bands.
        """
        if "Close" not in data.columns:
            logging.error("Missing 'Close' column in data.")
            return None

        sma = self.calculate_moving_average(data, period)
        std = data["Close"].rolling(window=period).std()

        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)

        logging.info("Calculated Bollinger Bands for %d-day period", period)
        return pd.DataFrame({"Upper_Band": upper_band, "Lower_Band": lower_band})

    def analyze_volatility(self, data, period=10):
        """
        Calculates rolling volatility.

        :param data: Pandas DataFrame with "Close" prices.
        :param period: Lookback period for volatility calculation.
        :return: Pandas Series with volatility values.
        """
        if "Close" not in data.columns:
            logging.error("Missing 'Close' column in data.")
            return None

        volatility = data["Close"].pct_change().rolling(window=period).std()
        logging.info("Calculated %d-day rolling volatility", period)
        return volatility

# Example Usage
if __name__ == "__main__":
    # Mock historical data
    data = pd.DataFrame({
        "Close": [2100, 2105, 2110, 2103, 2098, 2115, 2120, 2110, 2100, 2095]
    })

    analyzer = DataAnalyzer()

    print("50-day Moving Average:\n", analyzer.calculate_moving_average(data, period=50))
    print("14-day RSI:\n", analyzer.calculate_rsi(data, period=14))
    print("Bollinger Bands:\n", analyzer.calculate_bollinger_bands(data, period=20))
    print("Rolling Volatility:\n", analyzer.analyze_volatility(data, period=10))

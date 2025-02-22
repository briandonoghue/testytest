import logging
import pandas as pd
import numpy as np

class TechnicalIndicators:
    """
    TechnicalIndicators class computes common technical analysis indicators for a given asset's price data.
    Indicators include moving averages (SMA, EMA), RSI, MACD, and others.
    """

    def __init__(self, config):
        """
        Initializes the TechnicalIndicators class with configuration settings.
        :param config: Configuration dictionary containing settings for technical indicators.
        """
        self.config = config

        # Logging setup
        logging.basicConfig(
            filename="logs/technical_indicators.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def calculate_sma(self, data, window=14):
        """
        Calculates the Simple Moving Average (SMA).
        :param data: List or pandas Series of asset price data.
        :param window: The period over which to calculate the average.
        :return: pandas Series of SMA values.
        """
        sma = data.rolling(window=window).mean()
        logging.info(f"Calculated SMA with window size {window}")
        return sma

    def calculate_ema(self, data, window=14):
        """
        Calculates the Exponential Moving Average (EMA).
        :param data: List or pandas Series of asset price data.
        :param window: The period over which to calculate the average.
        :return: pandas Series of EMA values.
        """
        ema = data.ewm(span=window, adjust=False).mean()
        logging.info(f"Calculated EMA with window size {window}")
        return ema

    def calculate_rsi(self, data, window=14):
        """
        Calculates the Relative Strength Index (RSI).
        :param data: List or pandas Series of asset price data.
        :param window: The period over which to calculate the RSI.
        :return: pandas Series of RSI values.
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        logging.info(f"Calculated RSI with window size {window}")
        return rsi

    def calculate_macd(self, data, fast_window=12, slow_window=26, signal_window=9):
        """
        Calculates the Moving Average Convergence Divergence (MACD).
        :param data: List or pandas Series of asset price data.
        :param fast_window: The window for the fast EMA.
        :param slow_window: The window for the slow EMA.
        :param signal_window: The window for the signal line.
        :return: pandas Series of MACD values and Signal Line.
        """
        fast_ema = self.calculate_ema(data, fast_window)
        slow_ema = self.calculate_ema(data, slow_window)
        macd = fast_ema - slow_ema
        signal_line = self.calculate_ema(macd, signal_window)
        logging.info(f"Calculated MACD with fast window {fast_window}, slow window {slow_window}, and signal window {signal_window}")
        return macd, signal_line

    def calculate_bollinger_bands(self, data, window=20, num_std_dev=2):
        """
        Calculates Bollinger Bands.
        :param data: List or pandas Series of asset price data.
        :param window: The period over which to calculate the moving average.
        :param num_std_dev: The number of standard deviations to calculate the upper and lower bands.
        :return: pandas Series for Upper Band, Lower Band, and Moving Average.
        """
        sma = self.calculate_sma(data, window)
        rolling_std = data.rolling(window=window).std()
        upper_band = sma + (rolling_std * num_std_dev)
        lower_band = sma - (rolling_std * num_std_dev)
        logging.info(f"Calculated Bollinger Bands with window size {window} and {num_std_dev} standard deviations.")
        return upper_band, lower_band, sma

    def calculate_stochastic_oscillator(self, data, window=14):
        """
        Calculates the Stochastic Oscillator.
        :param data: List or pandas Series of asset price data.
        :param window: The period over which to calculate the stochastic oscillator.
        :return: pandas Series of %K values (Stochastic Oscillator).
        """
        low_min = data.rolling(window=window).min()
        high_max = data.rolling(window=window).max()
        stochastic_oscillator = 100 * ((data - low_min) / (high_max - low_min))
        logging.info(f"Calculated Stochastic Oscillator with window size {window}")
        return stochastic_oscillator

    def generate_all_indicators(self, data):
        """
        Generate all the technical indicators for a given asset price data.
        :param data: List or pandas Series of asset price data.
        :return: Dictionary containing all the calculated indicators.
        """
        indicators = {
            'sma': self.calculate_sma(data),
            'ema': self.calculate_ema(data),
            'rsi': self.calculate_rsi(data),
            'macd': self.calculate_macd(data)[0],
            'signal_line': self.calculate_macd(data)[1],
            'upper_band': self.calculate_bollinger_bands(data)[0],
            'lower_band': self.calculate_bollinger_bands(data)[1],
            'bollinger_ma': self.calculate_bollinger_bands(data)[2],
            'stochastic_oscillator': self.calculate_stochastic_oscillator(data)
        }
        logging.info("Generated all technical indicators.")
        return indicators

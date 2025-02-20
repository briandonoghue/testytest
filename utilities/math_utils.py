import logging
import numpy as np

class MathUtils:
    def __init__(self):
        """ Initializes the Math Utilities class. """
        # Setup logging
        logging.basicConfig(
            filename="logs/math_utils.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    @staticmethod
    def calculate_percentage_change(old_value, new_value):
        """ Calculates percentage change safely. """
        try:
            if old_value == 0:
                raise ValueError("Division by zero error in percentage change calculation.")
            return ((new_value - old_value) / old_value) * 100
        except Exception as e:
            logging.error("Error calculating percentage change: %s", e)
            return None

    @staticmethod
    def calculate_moving_average(data, period=10):
        """ Computes a simple moving average (SMA) over a given period. """
        try:
            if len(data) < period:
                raise ValueError("Not enough data points for moving average calculation.")
            return np.convolve(data, np.ones(period) / period, mode='valid')
        except Exception as e:
            logging.error("Error calculating moving average: %s", e)
            return None

    @staticmethod
    def calculate_standard_deviation(data):
        """ Computes standard deviation for risk analysis. """
        try:
            return np.std(data)
        except Exception as e:
            logging.error("Error calculating standard deviation: %s", e)
            return None

    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
        """ Computes Sharpe ratio for performance evaluation. """
        try:
            excess_returns = returns - risk_free_rate
            std_dev = np.std(returns)

            if std_dev == 0:
                raise ValueError("Standard deviation is zero, cannot calculate Sharpe ratio.")

            return np.mean(excess_returns) / std_dev
        except Exception as e:
            logging.error("Error calculating Sharpe ratio: %s", e)
            return None

# Example Usage
if __name__ == "__main__":
    math_utils = MathUtils()

    old_price = 2100
    new_price = 2150
    print("Percentage Change:", math_utils.calculate_percentage_change(old_price, new_price))

    price_data = [2100, 2105, 2110, 2103, 2098, 2115, 2120, 2110, 2100, 2095]
    print("Moving Average:", math_utils.calculate_moving_average(price_data, period=3))

    print("Standard Deviation:", math_utils.calculate_standard_deviation(price_data))

    returns = np.array([0.02, 0.01, -0.005, 0.03, -0.002])
    print("Sharpe Ratio:", math_utils.calculate_sharpe_ratio(returns))

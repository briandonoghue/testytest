import logging
import pandas as pd
import numpy as np

class PerformanceTracker:
    """ Tracks AI trading performance and risk metrics """

    def __init__(self, trade_log_file="logs/trade_history.csv"):
        """
        Initializes Performance Tracker.

        :param trade_log_file: Path to the AI trade history log.
        """
        self.trade_log_file = trade_log_file

        # Setup logging
        logging.basicConfig(
            filename="logs/performance_tracker.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def compute_performance_metrics(self):
        """ Computes AI trading performance metrics. """
        try:
            df = pd.read_csv(self.trade_log_file)

            if df.empty:
                logging.warning("No trade data found for performance tracking.")
                return {}

            df["Profit"] = df["Sell Price"] - df["Buy Price"]
            df["Cumulative Profit"] = df["Profit"].cumsum()

            total_trades = len(df)
            win_trades = len(df[df["Profit"] > 0])
            loss_trades = total_trades - win_trades
            win_rate = round((win_trades / total_trades) * 100, 2) if total_trades > 0 else 0

            total_profit = df["Profit"].sum()
            sharpe_ratio = self._calculate_sharpe_ratio(df["Profit"])
            max_drawdown = self._calculate_max_drawdown(df["Cumulative Profit"])
            profit_factor = round(df[df["Profit"] > 0]["Profit"].sum() / abs(df[df["Profit"] < 0]["Profit"].sum()), 2) if loss_trades > 0 else "N/A"

            performance_metrics = {
                "Total Trades": total_trades,
                "Win Rate (%)": win_rate,
                "Total Profit ($)": round(total_profit, 2),
                "Sharpe Ratio": round(sharpe_ratio, 2),
                "Max Drawdown ($)": round(max_drawdown, 2),
                "Profit Factor": profit_factor
            }

            logging.info("Performance Metrics Calculated: %s", performance_metrics)
            return performance_metrics

        except Exception as e:
            logging.error("Failed to compute performance metrics: %s", e)
            return {}

    def _calculate_sharpe_ratio(self, returns, risk_free_rate=0.01):
        """ Computes the Sharpe Ratio. """
        try:
            excess_returns = returns - risk_free_rate
            std_dev = np.std(returns)

            if std_dev == 0:
                return 0  # Avoid division by zero

            return np.mean(excess_returns) / std_dev

        except Exception as e:
            logging.error("Error calculating Sharpe ratio: %s", e)
            return 0

    def _calculate_max_drawdown(self, cumulative_profits):
        """ Computes the Maximum Drawdown (Largest Drop from Peak). """
        try:
            peak = cumulative_profits.cummax()
            drawdown = (cumulative_profits - peak)
            return drawdown.min()

        except Exception as e:
            logging.error("Error calculating max drawdown: %s", e)
            return 0

# Example Usage
if __name__ == "__main__":
    performance_tracker = PerformanceTracker()

    metrics = performance_tracker.compute_performance_metrics()
    if metrics:
        for key, value in metrics.items():
            print(f"{key}: {value}")

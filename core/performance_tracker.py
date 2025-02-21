import logging
import json
import os
import pandas as pd

class PerformanceTracker:
    """ Tracks AI trading performance, strategy success rates, and risk-adjusted returns. """

    def __init__(self, config):
        """
        Initializes the AI-driven performance tracker.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.trade_log_file = "logs/trade_log.json"
        self.performance_log_file = "logs/performance_metrics.json"

        # Ensure log directory exists
        os.makedirs("logs", exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename="logs/performance_tracker.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log_trade(self, trade_result):
        """
        Logs executed trades for AI performance analysis.
        :param trade_result: Dictionary containing executed trade details.
        """
        trade_data = self._load_trade_log()
        trade_data.append(trade_result)

        with open(self.trade_log_file, "w") as f:
            json.dump(trade_data, f, indent=4)

        logging.info(f"Logged trade: {trade_result}")

    def calculate_success_metrics(self):
        """
        Computes AI strategy performance metrics.
        :return: Dictionary of success metrics.
        """
        trade_data = self._load_trade_log()

        if not trade_data:
            return {"Win Rate": 0, "Profit Factor": 0, "Total Profit": 0, "Max Drawdown": 0}

        df = pd.DataFrame(trade_data)

        # Ensure required columns exist
        if "execution_price" not in df.columns or "status" not in df.columns:
            return {"Win Rate": 0, "Profit Factor": 0, "Total Profit": 0, "Max Drawdown": 0}

        # Calculate PnL for each trade
        df["pnl"] = df.apply(lambda row: row["execution_price"] * row["quantity"] if row["action"] == "buy" else -row["execution_price"] * row["quantity"], axis=1)

        # Define key metrics
        total_trades = len(df)
        winning_trades = len(df[df["pnl"] > 0])
        losing_trades = total_trades - winning_trades
        total_profit = df["pnl"].sum()
        max_drawdown = df["pnl"].min()
        profit_factor = total_profit / abs(df[df["pnl"] < 0]["pnl"].sum()) if losing_trades > 0 else 0
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

        success_metrics = {
            "Total Trades": total_trades,
            "Win Rate": round(win_rate, 2),
            "Profit Factor": round(profit_factor, 2),
            "Total Profit": round(total_profit, 2),
            "Max Drawdown": round(max_drawdown, 2)
        }

        # Save metrics
        with open(self.performance_log_file, "w") as f:
            json.dump(success_metrics, f, indent=4)

        logging.info(f"Updated AI performance metrics: {success_metrics}")
        return success_metrics

    def generate_performance_report(self):
        """
        Generates a trading performance report.
        :return: Dictionary of performance report data.
        """
        metrics = self.calculate_success_metrics()
        return metrics

    def _load_trade_log(self):
        """
        Loads existing trade history.
        :return: List of trade records.
        """
        try:
            with open(self.trade_log_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

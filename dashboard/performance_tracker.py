import os
import pandas as pd
import numpy as np

class PerformanceTracker:
    def __init__(self, trade_log_path="logs/trade_logs.txt", report_path="data/performance_report.csv"):
        """Initialize the performance tracker with file paths."""
        self.trade_log_path = trade_log_path
        self.report_path = report_path
        self.trades = self.load_trade_data()

    def load_trade_data(self):
        """Load trade history from trade logs."""
        if not os.path.exists(self.trade_log_path):
            print(f"❌ No trade log found at {self.trade_log_path}. Performance tracking unavailable.")
            return None

        df = pd.read_csv(self.trade_log_path)
        if "Date" not in df.columns or "Asset" not in df.columns or "PnL" not in df.columns:
            print(f"⚠️ Invalid trade log format. Expected columns: 'Date', 'Asset', 'PnL'.")
            return None

        df["Date"] = pd.to_datetime(df["Date"])
        return df

    def calculate_metrics(self):
        """Compute performance metrics like win rate, Sharpe ratio, and drawdown."""
        if self.trades is None or self.trades.empty:
            return None

        total_trades = len(self.trades)
        profitable_trades = self.trades[self.trades["PnL"] > 0]
        losing_trades = self.trades[self.trades["PnL"] < 0]
        win_rate = len(profitable_trades) / total_trades * 100 if total_trades > 0 else 0
        avg_profit = profitable_trades["PnL"].mean() if not profitable_trades.empty else 0
        avg_loss = losing_trades["PnL"].mean() if not losing_trades.empty else 0
        sharpe_ratio = self.calculate_sharpe_ratio()
        max_drawdown = self.calculate_max_drawdown()

        return {
            "Total Trades": total_trades,
            "Win Rate (%)": round(win_rate, 2),
            "Avg Profit ($)": round(avg_profit, 2),
            "Avg Loss ($)": round(avg_loss, 2),
            "Sharpe Ratio": round(sharpe_ratio, 2),
            "Max Drawdown ($)": round(max_drawdown, 2),
        }

    def calculate_sharpe_ratio(self, risk_free_rate=0.02):
        """Compute the Sharpe ratio based on daily returns."""
        if self.trades is None or self.trades.empty:
            return 0

        daily_returns = self.trades["PnL"].pct_change().dropna()
        return (daily_returns.mean() - risk_free_rate) / daily_returns.std() if not daily_returns.empty else 0

    def calculate_max_drawdown(self):
        """Calculate maximum drawdown based on cumulative returns."""
        if self.trades is None or self.trades.empty:
            return 0

        self.trades["Cumulative PnL"] = self.trades["PnL"].cumsum()
        peak = self.trades["Cumulative PnL"].cummax()
        drawdown = self.trades["Cumulative PnL"] - peak
        return drawdown.min()

    def generate_performance_report(self):
        """Generate a CSV performance report."""
        metrics = self.calculate_metrics()
        if metrics is None:
            return

        df = pd.DataFrame([metrics])
        df.to_csv(self.report_path, index=False)
        print(f"📊 Performance report saved to {self.report_path}")

    def display_metrics(self):
        """Display performance metrics in a readable format."""
        metrics = self.calculate_metrics()
        if metrics is None:
            print("⚠️ No trade data available.")
            return

        print("\n📈 Trading Performance Summary:")
        for key, value in metrics.items():
            print(f"  ✅ {key}: {value}")

# ✅ Example Usage
if __name__ == "__main__":
    tracker = PerformanceTracker()
    tracker.generate_performance_report()
    tracker.display_metrics()

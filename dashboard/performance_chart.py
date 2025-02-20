import os
import pandas as pd
import matplotlib.pyplot as plt

# ✅ Ensure matplotlib works in headless environments
plt.switch_backend('Agg')

class PerformanceChart:
    def __init__(self, data_dir="data", output_dir="charts"):
        """Initialize performance chart generator."""
        self.data_dir = data_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # ✅ Ensure output directory exists

    def load_trade_results(self):
        """Load trade performance data."""
        file_path = os.path.join(self.data_dir, "paper_trading_results.csv")
        if not os.path.exists(file_path):
            print(f"❌ No trade results found at {file_path}. Generating an empty chart.")
            return None

        df = pd.read_csv(file_path)
        if "Date" not in df.columns or "Balance" not in df.columns:
            print(f"⚠️ Invalid trade results format. Expected columns: 'Date', 'Balance'.")
            return None

        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        return df

    def plot_equity_curve(self, df):
        """Generate an equity curve plot based on trading performance."""
        if df is None or df.empty:
            return

        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df["Balance"], label="Equity Curve", color="blue", linewidth=2)
        plt.axhline(y=df["Balance"].iloc[0], color="gray", linestyle="--", label="Starting Balance")
        plt.title("Trading Performance: Equity Curve")
        plt.xlabel("Date")
        plt.ylabel("Balance ($)")
        plt.legend()
        plt.grid(True)

        file_path = os.path.join(self.output_dir, "equity_curve.png")
        plt.savefig(file_path)
        print(f"📈 Equity curve saved to {file_path}")

    def plot_drawdown(self, df):
        """Generate a drawdown chart to analyze risk."""
        if df is None or df.empty:
            return

        df["Peak"] = df["Balance"].cummax()
        df["Drawdown"] = df["Balance"] - df["Peak"]

        plt.figure(figsize=(12, 6))
        plt.fill_between(df.index, df["Drawdown"], color="red", alpha=0.3)
        plt.title("Trading Performance: Drawdown Over Time")
        plt.xlabel("Date")
        plt.ylabel("Drawdown ($)")
        plt.grid(True)

        file_path = os.path.join(self.output_dir, "drawdown_chart.png")
        plt.savefig(file_path)
        print(f"📉 Drawdown chart saved to {file_path}")

    def plot_monthly_returns(self, df):
        """Generate a bar chart of monthly returns."""
        if df is None or df.empty:
            return

        df["Monthly Return"] = df["Balance"].pct_change(freq="M") * 100

        plt.figure(figsize=(12, 6))
        df["Monthly Return"].plot(kind="bar", color="green", alpha=0.7)
        plt.title("Trading Performance: Monthly Returns (%)")
        plt.xlabel("Month")
        plt.ylabel("Return (%)")
        plt.grid(True)

        file_path = os.path.join(self.output_dir, "monthly_returns.png")
        plt.savefig(file_path)
        print(f"📊 Monthly returns chart saved to {file_path}")

    def generate_all_charts(self):
        """Run all chart generation methods."""
        df = self.load_trade_results()
        if df is not None:
            self.plot_equity_curve(df)
            self.plot_drawdown(df)
            self.plot_monthly_returns(df)

# ✅ Example Usage
if __name__ == "__main__":
    chart_generator = PerformanceChart()
    chart_generator.generate_all_charts()

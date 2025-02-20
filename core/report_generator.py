import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from performance_tracker import PerformanceTracker

class ReportGenerator:
    """ Generates AI Trading Performance Reports """

    def __init__(self, trade_log_file="logs/trade_history.csv", report_dir="reports/"):
        self.trade_log_file = trade_log_file
        self.report_dir = report_dir
        self.performance_tracker = PerformanceTracker()

        # Ensure report directory exists
        import os
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        # Setup logging
        logging.basicConfig(
            filename="logs/report_generator.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def generate_report(self):
        """ Generates an AI performance report with key metrics and charts. """
        try:
            df = pd.read_csv(self.trade_log_file)

            if df.empty:
                logging.warning("No trade data found for report generation.")
                return None

            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            
            # Performance Metrics
            performance_metrics = self.performance_tracker.compute_performance_metrics()
            self._generate_pdf_report(df, performance_metrics)

            # Generate Charts
            self._plot_profit_curve(df)
            self._plot_trade_distribution(df)

            logging.info("AI Performance Report Generated Successfully.")
            return f"{self.report_dir}ai_performance_report.pdf"

        except Exception as e:
            logging.error("Failed to generate report: %s", e)
            return None

    def _generate_pdf_report(self, df, performance_metrics):
        """ Creates a PDF performance report with metrics and charts. """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "AI Trading Performance Report", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.ln(10)

        for key, value in performance_metrics.items():
            pdf.cell(200, 10, f"{key}: {value}", ln=True)

        pdf.ln(10)
        pdf.image("reports/profit_curve.png", x=10, w=180)
        pdf.ln(5)
        pdf.image("reports/trade_distribution.png", x=10, w=180)

        pdf.output(f"{self.report_dir}ai_performance_report.pdf")

    def _plot_profit_curve(self, df):
        """ Plots the profit curve of AI trading. """
        df["Cumulative Profit"] = df["Profit"].cumsum()
        plt.figure(figsize=(10, 5))
        plt.plot(df["Timestamp"], df["Cumulative Profit"], label="AI Cumulative Profit", linewidth=2)
        plt.xlabel("Time")
        plt.ylabel("Cumulative Profit ($)")
        plt.title("AI Profit Curve Over Time")
        plt.legend()
        plt.grid()
        plt.savefig("reports/profit_curve.png")
        plt.close()

    def _plot_trade_distribution(self, df):
        """ Plots trade distribution (win/loss) for AI trades. """
        win_trades = df[df["Profit"] > 0]
        loss_trades = df[df["Profit"] < 0]

        labels = ["Win Trades", "Loss Trades"]
        sizes = [len(win_trades), len(loss_trades)]
        colors = ["green", "red"]

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
        plt.title("AI Trading Win/Loss Distribution")
        plt.savefig("reports/trade_distribution.png")
        plt.close()

# Run Report Generation
if __name__ == "__main__":
    report_generator = ReportGenerator()
    report_file = report_generator.generate_report()

    if report_file:
        print(f"✅ AI Performance Report Generated: {report_file}")

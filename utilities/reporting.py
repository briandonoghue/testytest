import logging
import json
import os
import pandas as pd
from fpdf import FPDF
from core.risk_manager import RiskManager
from core.performance_tracker import PerformanceTracker
from core.market_data import MarketData

class Reporting:
    """ Generates AI-driven risk reports for portfolio analysis """

    def __init__(self, config):
        """
        Initializes the AI-driven reporting system.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.performance_tracker = PerformanceTracker(config)
        self.risk_manager = RiskManager(config)
        self.market_data = MarketData(config)
        self.report_directory = "reports"

        # Ensure report directory exists
        os.makedirs(self.report_directory, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename="logs/reporting.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def generate_risk_report(self):
        """
        Generates an AI-driven risk analysis report.
        :return: Risk report dictionary.
        """
        logging.info("Generating AI-driven risk report...")

        performance_metrics = self.performance_tracker.generate_performance_report()
        portfolio_allocation = self.risk_manager.analyze_portfolio_allocation()
        market_volatility = {symbol: self.market_data.get_asset_volatility(symbol) for symbol in portfolio_allocation.keys()}

        risk_report = {
            "performance_metrics": performance_metrics,
            "portfolio_allocation": portfolio_allocation,
            "market_volatility": market_volatility,
            "recommended_rebalancing": self.risk_manager.rebalance_portfolio()
        }

        report_path = os.path.join(self.report_directory, "risk_report.json")
        with open(report_path, "w") as f:
            json.dump(risk_report, f, indent=4)

        logging.info(f"AI Risk Report saved to {report_path}")
        return risk_report

    def generate_pdf_report(self):
        """
        Creates a PDF report with AI-driven risk and performance insights.
        """
        risk_data = self.generate_risk_report()
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, "AI Trading Risk & Performance Report", ln=True, align="C")
        pdf.ln(10)

        # Add Performance Metrics
        pdf.set_font("Arial", "B", 10)
        pdf.cell(200, 10, "Performance Metrics", ln=True)
        pdf.set_font("Arial", size=10)
        for key, value in risk_data["performance_metrics"].items():
            pdf.cell(200, 8, f"{key}: {value}", ln=True)

        pdf.ln(10)

        # Add Portfolio Allocation
        pdf.set_font("Arial", "B", 10)
        pdf.cell(200, 10, "Portfolio Allocation", ln=True)
        pdf.set_font("Arial", size=10)
        for asset, allocation in risk_data["portfolio_allocation"].items():
            pdf.cell(200, 8, f"{asset}: {allocation}%", ln=True)

        pdf.ln(10)

        # Add Market Volatility
        pdf.set_font("Arial", "B", 10)
        pdf.cell(200, 10, "Market Volatility", ln=True)
        pdf.set_font("Arial", size=10)
        for asset, volatility in risk_data["market_volatility"].items():
            pdf.cell(200, 8, f"{asset}: {volatility:.2f}", ln=True)

        pdf.ln(10)

        # Add Recommended Rebalancing
        pdf.set_font("Arial", "B", 10)
        pdf.cell(200, 10, "AI Recommended Rebalancing", ln=True)
        pdf.set_font("Arial", size=10)
        if risk_data["recommended_rebalancing"]:
            for rebalance in risk_data["recommended_rebalancing"]:
                pdf.cell(200, 8, f"{rebalance['symbol']}: {rebalance['adjustment'] * 100:.2f}% change", ln=True)
        else:
            pdf.cell(200, 8, "No rebalancing required.", ln=True)

        # Save PDF
        pdf_path = os.path.join(self.report_directory, "AI_Risk_Performance_Report.pdf")
        pdf.output(pdf_path)
        logging.info(f"AI Risk & Performance PDF Report saved to {pdf_path}")

        return pdf_path

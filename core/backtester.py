import logging
import pandas as pd
import numpy as np
from core.market_data import MarketData
from core.risk_manager import RiskManager
from utilities.config_loader import load_config

class Backtester:
    """ AI-powered backtesting system for evaluating trading strategies. """

    def __init__(self, config):
        """
        Initializes the backtester with AI-driven enhancements.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.risk_manager = RiskManager(config)
        self.initial_balance = config.get("backtester", {}).get("starting_balance", 10000)
        self.current_balance = self.initial_balance
        self.trade_log = []

        # Setup logging
        logging.basicConfig(
            filename="logs/backtester.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def _simulate_trade_execution(self, trade_signal):
        """
        Simulates trade execution with AI-based slippage and realistic fills.
        :param trade_signal: Dictionary containing trade details.
        :return: Adjusted execution price.
        """
        if not self.risk_manager.evaluate_risk(trade_signal):
            logging.warning(f"Trade rejected by risk management: {trade_signal}")
            return None

        symbol = trade_signal["symbol"]
        action = trade_signal["action"]
        quantity = trade_signal["quantity"]
        trade_price = trade_signal["price"]

        # Apply AI-based slippage model
        slippage_factor = np.random.uniform(0.995, 1.005)  # Simulated slippage
        execution_price = trade_price * slippage_factor

        # Log trade details
        trade_record = {
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "entry_price": execution_price,
            "trade_cost": execution_price * quantity
        }
        self.trade_log.append(trade_record)

        logging.info(f"Simulated trade executed: {trade_record}")
        return execution_price

    def run_backtest(self, strategy_engine):
        """
        Runs backtesting on AI-driven trading strategies.
        :param strategy_engine: Instance of StrategyEngine for generating signals.
        """
        logging.info("Running AI-driven backtest...")

        for iteration in range(100):  # Simulate 100 trading cycles
            trade_signals = strategy_engine.generate_signals()

            for trade_signal in trade_signals:
                execution_price = self._simulate_trade_execution(trade_signal)
                if execution_price:
                    if trade_signal["action"] == "buy":
                        self.current_balance -= execution_price * trade_signal["quantity"]
                    else:  # Sell order
                        self.current_balance += execution_price * trade_signal["quantity"]

            logging.info(f"Iteration {iteration + 1} - Account Balance: {self.current_balance:.2f}")

        logging.info("Backtest completed.")
        self._generate_performance_report()

    def _generate_performance_report(self):
        """
        Generates an AI-based performance report for strategy evaluation.
        """
        if not self.trade_log:
            logging.warning("No trades executed during backtest.")
            return

        df = pd.DataFrame(self.trade_log)

        df["profit_loss"] = np.where(df["action"] == "sell",
                                     (df["entry_price"] - df["entry_price"].shift(1)) * df["quantity"], 0)
        total_profit = df["profit_loss"].sum()
        max_drawdown = (df["entry_price"].max() - df["entry_price"].min()) / df["entry_price"].max()
        win_rate = df[df["profit_loss"] > 0].shape[0] / max(1, df.shape[0])

        report = {
            "Total Profit": round(total_profit, 2),
            "Max Drawdown": round(max_drawdown * 100, 2),
            "Win Rate": round(win_rate * 100, 2),
            "Final Balance": round(self.current_balance, 2)
        }

        logging.info(f"Backtest Report: {report}")
        print("\n📊 AI Backtest Report 📊")
        for key, value in report.items():
            print(f"{key}: {value}")

        return report

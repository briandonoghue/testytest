import logging
import threading
import time
import pandas as pd
import json
from flask import Flask, render_template, jsonify
from core.performance_tracker import PerformanceTracker
from core.market_data import MarketData
from core.trade_executor import TradeExecutor
from core.risk_manager import RiskManager
from core.order_manager import OrderManager
from utilities.config_loader import load_config

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config = load_config("config/config.json")

# Initialize components
performance_tracker = PerformanceTracker(config)
market_data = MarketData(config)
trade_executor = TradeExecutor(config)
risk_manager = RiskManager(config)
order_manager = OrderManager(config)

# Setup logging
logging.basicConfig(
    filename="logs/dashboard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/")
def home():
    """ Renders the AI trading dashboard. """
    return render_template("index.html")

@app.route("/performance")
def get_performance_data():
    """ Returns AI trading performance metrics for visualization. """
    report = performance_tracker.generate_performance_report()
    return jsonify(report)

@app.route("/market_data/<symbol>")
def get_market_data(symbol):
    """ Returns real-time market price of an asset. """
    price = market_data.get_latest_price(symbol)
    return jsonify({"symbol": symbol, "price": price})

@app.route("/trade/<symbol>/<action>/<quantity>")
def execute_trade(symbol, action, quantity):
    """ Manually execute a trade from the dashboard. """
    trade_signal = {
        "symbol": symbol,
        "action": action,
        "quantity": float(quantity),
        "price": market_data.get_latest_price(symbol)
    }
    execution_result = trade_executor.execute_order(trade_signal)
    return jsonify(execution_result)

@app.route("/trade_history")
def get_trade_history():
    """ Fetches executed trade history for visualization. """
    try:
        with open("logs/trade_log.json", "r") as f:
            trade_history = json.load(f)
        return jsonify(trade_history)
    except Exception as e:
        logging.error(f"Error retrieving trade history: {e}")
        return jsonify([])

@app.route("/ai_trade_confidence")
def get_ai_trade_confidence():
    """ Retrieves AI confidence levels for the latest trade signals. """
    try:
        with open("logs/trade_log.json", "r") as f:
            trade_history = json.load(f)
        
        confidence_scores = [{"symbol": trade["symbol"], "confidence": trade.get("confidence", 0.5)} for trade in trade_history]
        return jsonify(confidence_scores)
    except Exception as e:
        logging.error(f"Error retrieving AI trade confidence levels: {e}")
        return jsonify([])

@app.route("/risk_exposure")
def get_risk_exposure():
    """ Retrieves AI-calculated risk exposure across all assets. """
    portfolio_risk = risk_manager.calculate_portfolio_risk()
    return jsonify(portfolio_risk)

def run_dashboard():
    """ Starts the Flask dashboard server. """
    app.run(host="0.0.0.0", port=config["dashboard"].get("port", 8080), debug=False, threaded=True)

# Run dashboard in a separate thread
dashboard_thread = threading.Thread(target=run_dashboard)
dashboard_thread.daemon = True
dashboard_thread.start()

if __name__ == "__main__":
    logging.info("Starting AI Trading Bot Dashboard...")
    while True:
        time.sleep(10)  # Keeps the script running

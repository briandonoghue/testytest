import logging
import json
from trade_executor import TradeExecutor
from trade_signal_generator import TradeSignalGenerator
from ml_self_training import MLSelfTrainer
from ai_trade_confidence import AITradeConfidenceScorer
from ai_trade_explanation import AITradeExplanation
from market_anomaly_detection import MarketAnomalyDetector
from ai_position_sizing import AIPositionSizer
from ai_market_regime_adaptation import AIMarketRegimeAdapter
from ai_trade_timing import AITradeTimingOptimizer
from ai_liquidity_tracking import AILiquidityTracker
from ai_stop_loss_optimization import AIStopLossOptimizer
from ai_take_profit_optimization import AITakeProfitOptimizer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load configuration
with open("config/config.json", "r") as f:
    config = json.load(f)

# Initialize core AI components
trade_execution = TradeExecutor(config)
trade_signal_generator = TradeSignalGenerator(config)
ml_trainer = MLSelfTrainer(config)
confidence_scorer = AITradeConfidenceScorer(config)
trade_explainer = AITradeExplanation(config)
anomaly_detector = MarketAnomalyDetector(config)
position_sizer = AIPositionSizer(config)
market_adapter = AIMarketRegimeAdapter(config)
timing_optimizer = AITradeTimingOptimizer(config)
liquidity_tracker = AILiquidityTracker(config)
stop_loss_optimizer = AIStopLossOptimizer(config)
take_profit_optimizer = AITakeProfitOptimizer(config)

def main():
    logging.info("🔹 AI Trading Bot Starting...")
    
    # Step 1: Detect Market Regime and Adjust Strategy
    logging.info("📊 Detecting current market regime...")
    
    trading_assets = config["assets"]["primary_assets"]
    
    for asset in trading_assets:
        # Get market conditions for the current asset
        market_conditions = trade_execution.market_data.get_market_conditions(symbol=asset)
        
        # Detect market regime based on the market conditions
        market_regime = market_adapter.detect_market_regime(market_conditions)
        logging.info(f"✅ Market Regime Identified for {asset}: {market_regime}")

        # Step 2: Select the Best Strategy Based on Market Regime
        selected_strategy = market_adapter.adapt_strategy_to_market(market_conditions)
        logging.info(f"🛠️ Using Strategy for {asset}: {selected_strategy['type']}")

        # Step 3: Generate Trade Signals
        logging.info(f"📊 Generating trade signal for {asset}...")
        trade_signal = trade_signal_generator.generate_signal(asset, selected_strategy)

        # Step 4: Calculate Trade Confidence Score
        confidence_score = confidence_scorer.calculate_confidence_score(trade_signal)
        logging.info(f"🔎 Trade Confidence Score for {asset}: {confidence_score:.2f}")

        if confidence_score < config["trading_settings"]["min_confidence_threshold"]:
            logging.info(f"⚠️ Skipping trade for {asset} due to low confidence.")
            continue

        # Step 5: Explain Trade Decision
        trade_explanation = trade_explainer.generate_explanation(trade_signal)
        logging.info(f"📝 Trade Explanation for {asset}: {trade_explanation}")

        # Step 6: Detect Market Anomalies
        anomaly_detected = anomaly_detector.check_market_anomalies(asset)
        if anomaly_detected:
            logging.warning(f"🚨 Market anomaly detected for {asset}. Skipping trade.")
            continue

        # Step 7: Determine Optimal Trade Size
        position_size = position_sizer.calculate_trade_size({
            "symbol": asset,
            "account_balance": trade_execution.get_account_balance(),
            "risk_per_trade": config["risk_management"]["max_trade_risk"],
            "stop_loss_distance": trade_signal.get("stop_loss_distance", 0)
        })
        logging.info(f"📏 Calculated Trade Size for {asset}: {position_size}")

        # Step 8: Optimize Entry Timing
        optimized_entry = timing_optimizer.identify_best_entry_time(trade_signal)
        if optimized_entry["execution_timing"] == "DELAYED":
            logging.info(f"🕒 Delaying trade execution for {asset} due to market conditions.")
            continue

        # Step 9: Optimize Take-Profit and Stop-Loss Levels
        optimized_stop_loss = stop_loss_optimizer.calculate_dynamic_stop_loss(trade_signal)
        optimized_take_profit = take_profit_optimizer.calculate_dynamic_take_profit(trade_signal)
        logging.info(f"📉 Optimized Stop-Loss: {optimized_stop_loss} | 📈 Optimized Take-Profit: {optimized_take_profit}")

        # Step 10: Execute Trade
        execution_result = trade_execution.execute_trade(trade_signal, market_regime, stop_loss=optimized_stop_loss, take_profit=optimized_take_profit)
        if execution_result:
            logging.info(f"✅ Trade executed successfully for {asset}.")
        else:
            logging.error(f"❌ Trade execution failed for {asset}.")

    # Step 11: AI Self-Retraining (Only if Needed)
    retraining_needed = ml_trainer.check_retraining_need()
    if retraining_needed:
        logging.info("🔄 Retraining AI Model...")
        ml_trainer.train_model()

    logging.info("🚀 AI Trading Bot Execution Completed.")


if __name__ == "__main__":
    main()

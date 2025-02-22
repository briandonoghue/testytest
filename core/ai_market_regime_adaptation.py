import logging
import numpy as np
from market_data import MarketData
from ai_position_sizing import AIPositionSizer
from trade_executor import TradeExecutor

class AIMarketRegimeAdapter:
    """AI-driven market regime adaptation for adjusting trading strategies based on market conditions."""

    def __init__(self, config):
        """
        Initializes the market regime adaptation system.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.position_sizer = AIPositionSizer(config)
        self.trade_executor = TradeExecutor(config)

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_market_regime_adapter.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def detect_market_regime(self, market_conditions):
        """
        Detects the current market regime based on key indicators like price momentum, volatility, etc.
        :param market_conditions: Dictionary containing market data and conditions.
        :return: String indicating the market regime (e.g., "bull", "bear", "neutral").
        """

 
        if market_conditions is None:
            logging.error("Market conditions are None. Cannot detect market regime.")
        return None
        # Calculate relevant indicators (e.g., price change, volatility, moving averages)
        price_change = self.market_data.get_price_change_percentage(market_conditions["symbol"])
        volatility = self.market_data.get_asset_volatility(market_conditions["symbol"])

        # Determine market regime based on price change and volatility
        if price_change > self.config["market_conditions"]["bull_threshold"] and volatility < self.config["market_conditions"]["volatility_threshold"]:
            return "bull"
        elif price_change < self.config["market_conditions"]["bear_threshold"] and volatility < self.config["market_conditions"]["volatility_threshold"]:
            return "bear"
        else:
            return "neutral"

    def adapt_strategy_to_market(self, market_conditions):
        """
        Adapts the trading strategy based on the detected market regime.
        :param market_conditions: Dictionary containing market data and conditions.
        :return: Adapted strategy dictionary.
        """

        if market_conditions is None:
            logging.error("Market conditions are None. Cannot detect market regime.")
        return None

        market_regime = self.detect_market_regime(market_conditions)
        logging.info(f"Detected market regime: {market_regime}")

        strategy = {}
        
        if market_regime == "bull":
            strategy = self.config["strategies"]["bull_market"]
            logging.info("Using Bull Market Strategy.")
        elif market_regime == "bear":
            strategy = self.config["strategies"]["bear_market"]
            logging.info("Using Bear Market Strategy.")
        else:
            strategy = self.config["strategies"]["neutral_market"]
            logging.info("Using Neutral Market Strategy.")

        return strategy

    def execute_adapted_strategy(self, asset, strategy, account_balance):
        """
        Executes the adapted strategy based on market regime for a specific asset.
        :param asset: The trading asset symbol (e.g., 'AAPL').
        :param strategy: The adapted strategy dictionary.
        :param account_balance: The account balance for calculating position size.
        :return: Execution result of the trade.
        """
        # Calculate position size based on strategy and market conditions
        stop_loss_distance = strategy.get("stop_loss_distance", 0.02)  # Default 2% stop loss
        trade_params = {
            "symbol": asset,
            "account_balance": account_balance,
            "risk_per_trade": strategy.get("risk_per_trade", 0.02),  # Default 2% risk per trade
            "stop_loss_distance": stop_loss_distance
        }

        position_size = self.position_sizer.calculate_trade_size(trade_params)
        position_size = self.position_sizer.adjust_for_market_conditions(asset, position_size)

        # Define the trade signal
        trade_signal = {
            "symbol": asset,
            "action": strategy["action"],
            "quantity": position_size,
            "price": self.market_data.get_latest_price(asset),
            "stop_loss_distance": stop_loss_distance
        }

        # Execute the trade using the trade executor
        execution_result = self.trade_executor.execute_order(trade_signal)

        return execution_result

import logging
import numpy as np
from market_data import MarketData
from risk_manager import RiskManager

class AIPositionSizer:
    """AI-driven position sizing based on account balance, risk management, and market conditions."""

    def __init__(self, config):
        """
        Initializes the position sizing system.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.risk_manager = RiskManager(config)

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_position_sizer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def calculate_trade_size(self, trade_params):
        """
        Calculates the optimal position size based on available balance, risk per trade, and stop-loss distance.
        :param trade_params: Dictionary containing trading parameters like symbol, balance, risk, stop_loss_distance.
        :return: Optimal position size.
        """
        symbol = trade_params["symbol"]
        account_balance = trade_params["account_balance"]
        risk_per_trade = trade_params["risk_per_trade"]
        stop_loss_distance = trade_params["stop_loss_distance"]

        # If no stop-loss distance is provided, use default value
        if stop_loss_distance == 0:
            stop_loss_distance = self.config["risk_management"].get("default_stop_loss_distance", 1.0)

        # Calculate the dollar amount to risk per trade
        dollar_risk = account_balance * risk_per_trade

        # Fetch the latest market price for the symbol
        market_price = self.market_data.get_latest_price(symbol)
        if market_price is None:
            logging.error(f"Unable to fetch market data for {symbol}. Skipping position sizing.")
            return None

        # Calculate the position size based on the stop-loss distance and risk per trade
        position_size = dollar_risk / (market_price * stop_loss_distance)
        position_size = np.floor(position_size)  # Round down to avoid partial contracts

        logging.info(f"Calculated Position Size for {symbol}: {position_size} units")

        return position_size

    def adjust_for_market_conditions(self, symbol, position_size):
        """
        Adjusts position size based on current market conditions like volatility or liquidity.
        :param symbol: Trading asset symbol.
        :param position_size: Initially calculated position size.
        :return: Adjusted position size based on market conditions.
        """
        market_volatility = self.market_data.get_asset_volatility(symbol)
        market_liquidity = self.market_data.get_asset_liquidity(symbol)

        # Adjust the position size based on volatility (reduce position in high volatility)
        volatility_factor = 1.0
        if market_volatility > self.config["market_conditions"]["high_volatility_threshold"]:
            volatility_factor = 0.5  # Reduce position size by 50% in high volatility
            logging.warning(f"High volatility detected for {symbol}. Reducing position size.")

        # Adjust the position size based on liquidity (reduce position in low liquidity)
        liquidity_factor = 1.0
        if market_liquidity < self.config["market_conditions"]["low_liquidity_threshold"]:
            liquidity_factor = 0.75  # Reduce position size by 25% in low liquidity
            logging.warning(f"Low liquidity detected for {symbol}. Reducing position size.")

        # Apply market condition adjustments
        adjusted_position_size = position_size * volatility_factor * liquidity_factor
        adjusted_position_size = np.floor(adjusted_position_size)  # Round down to avoid partial contracts

        logging.info(f"Adjusted Position Size for {symbol}: {adjusted_position_size} units")

        return adjusted_position_size


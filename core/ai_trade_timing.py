import logging
import numpy as np
from market_data import MarketData
from ai_position_sizing import AIPositionSizer
from trade_executor import TradeExecutor
from datetime import datetime, timedelta

class AITradeTimingOptimizer:
    """AI-driven trade timing optimization for executing trades at optimal moments."""

    def __init__(self, config):
        """
        Initializes the trade timing optimizer.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.market_data = MarketData(config)
        self.position_sizer = AIPositionSizer(config)
        self.trade_executor = TradeExecutor(config)

        # Setup logging
        logging.basicConfig(
            filename="logs/ai_trade_timing_optimizer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def identify_best_entry_time(self, trade_signal):
        """
        Identifies the best entry time for executing a trade based on market conditions.
        :param trade_signal: The trade signal containing information about the asset and trade.
        :return: A dictionary with the best execution timing and any necessary delays.
        """
        symbol = trade_signal["symbol"]
        current_time = datetime.now()

        # Check if it's within optimal market hours for the asset
        market_open_time = self.market_data.get_market_open_time(symbol)
        market_close_time = self.market_data.get_market_close_time(symbol)

        if current_time < market_open_time or current_time > market_close_time:
            # Wait for the market to open or close before executing the trade
            execution_timing = "DELAYED"
            delay = self._calculate_delay(market_open_time)
            logging.info(f"Delaying execution for {symbol} until market opens.")
        else:
            execution_timing = "IMMEDIATE"
            delay = 0  # No delay needed if it's during market hours
            logging.info(f"Executing trade for {symbol} immediately.")

        # Optionally, adjust the execution timing based on volatility, liquidity, or other factors
        adjusted_timing, adjusted_delay = self._apply_market_conditions_adjustment(symbol, execution_timing, delay)

        return {"execution_timing": adjusted_timing, "execution_delay": adjusted_delay}

    def _calculate_delay(self, market_open_time):
        """
        Calculates the delay needed until market open.
        :param market_open_time: The time when the market opens.
        :return: Delay time in seconds.
        """
        time_to_wait = market_open_time - datetime.now()
        return max(0, time_to_wait.total_seconds())

    def _apply_market_conditions_adjustment(self, symbol, execution_timing, delay):
        """
        Optionally adjust the execution timing based on factors like volatility and liquidity.
        :param symbol: The trading asset symbol.
        :param execution_timing: The initial execution timing ('IMMEDIATE' or 'DELAYED').
        :param delay: The calculated delay time.
        :return: Adjusted execution timing and delay.
        """
        market_price = self.market_data.get_latest_price(symbol)
        volatility = self.market_data.get_asset_volatility(symbol)

        # If volatility is high, we might delay the execution for more favorable conditions
        if volatility > self.config["trade_conditions"]["volatility_threshold"]:
            adjusted_execution_timing = "DELAYED"
            adjusted_delay = delay + np.random.uniform(0.1, 0.5)  # Add a random delay to avoid sudden market moves
            logging.info(f"High volatility detected for {symbol}, delaying execution.")
        else:
            adjusted_execution_timing = execution_timing
            adjusted_delay = delay

        return adjusted_execution_timing, adjusted_delay

    def execute_trade_with_timing(self, trade_signal, execution_timing, delay):
        """
        Executes the trade based on the identified optimal timing.
        :param trade_signal: The trade signal.
        :param execution_timing: The timing for executing the trade.
        :param delay: Delay time before executing the trade.
        :return: The execution result.
        """
        # If execution is delayed, wait before executing
        if execution_timing == "DELAYED":
            logging.info(f"Delaying trade execution for {trade_signal['symbol']} by {delay} seconds.")
            time.sleep(delay)

        # Execute the trade when timing is optimal
        execution_result = self.trade_executor.execute_order(trade_signal)
        return execution_result

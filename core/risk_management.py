import logging

class RiskManagement:
    """
    Risk Management module to ensure trades adhere to predefined risk constraints.
    Includes position sizing, stop-loss, and portfolio exposure limits.
    """

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger("RiskManagement")

        # Load risk parameters from configuration
        self.max_risk_per_trade = self.config.get("max_risk_per_trade", 0.01)  # 1% default
        self.max_daily_drawdown = self.config.get("max_daily_drawdown", 0.05)  # 5% default
        self.max_exposure = self.config.get("max_exposure", 0.5)  # 50% default
        self.use_trailing_stop = self.config.get("use_trailing_stop", True)
        self.trailing_stop_percent = self.config.get("trailing_stop_percent", 0.02)  # 2% default
        self.log.info("Risk Management initialized with parameters: %s", self.config)

    def calculate_position_size(self, account_balance, stop_loss_distance):
        """
        Calculate position size based on risk per trade.

        Args:
            account_balance (float): Current account balance.
            stop_loss_distance (float): Distance of stop loss in %.

        Returns:
            float: Maximum position size in units.
        """
        risk_amount = account_balance * self.max_risk_per_trade
        if stop_loss_distance <= 0:
            self.log.warning("Invalid stop loss distance. Returning zero position size.")
            return 0

        position_size = risk_amount / stop_loss_distance
        self.log.info("Calculated position size: %.2f units", position_size)
        return position_size

    def apply_stop_loss(self, entry_price, direction):
        """
        Apply stop-loss based on strategy settings.

        Args:
            entry_price (float): Price at which the trade is executed.
            direction (str): 'long' or 'short'

        Returns:
            float: Stop-loss price.
        """
        if direction.lower() == "long":
            stop_loss = entry_price * (1 - self.max_risk_per_trade)
        else:
            stop_loss = entry_price * (1 + self.max_risk_per_trade)

        self.log.info("Stop-loss set at %.2f", stop_loss)
        return stop_loss

    def apply_trailing_stop(self, current_price, entry_price, direction):
        """
        Apply a trailing stop loss.

        Args:
            current_price (float): Current market price.
            entry_price (float): Trade entry price.
            direction (str): 'long' or 'short'

        Returns:
            float: New stop-loss price.
        """
        if not self.use_trailing_stop:
            return None

        if direction.lower() == "long":
            trailing_stop = max(entry_price, current_price * (1 - self.trailing_stop_percent))
        else:
            trailing_stop = min(entry_price, current_price * (1 + self.trailing_stop_percent))

        self.log.info("Trailing stop updated to %.2f", trailing_stop)
        return trailing_stop

    def check_drawdown_limit(self, current_balance, initial_balance):
        """
        Checks if the max daily drawdown limit is breached.

        Args:
            current_balance (float): Current account balance.
            initial_balance (float): Account balance at start of day.

        Returns:
            bool: True if drawdown limit exceeded, False otherwise.
        """
        drawdown = (initial_balance - current_balance) / initial_balance
        if drawdown >= self.max_daily_drawdown:
            self.log.warning("Max daily drawdown exceeded! Trading should be halted.")
            return True
        return False

    def check_exposure_limit(self, total_exposure, account_balance):
        """
        Ensure portfolio exposure does not exceed the max allowed.

        Args:
            total_exposure (float): Total value of open positions.
            account_balance (float): Current account balance.

        Returns:
            bool: True if exposure limit exceeded, False otherwise.
        """
        exposure_ratio = total_exposure / account_balance
        if exposure_ratio > self.max_exposure:
            self.log.warning("Exposure limit exceeded! Consider reducing position sizes.")
            return True
        return False

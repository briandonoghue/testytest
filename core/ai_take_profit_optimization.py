# core/ai_take_profit_optimization.py

import numpy as np
import pandas as pd

class AITakeProfitOptimizer:
    def __init__(self, config):
        self.config = config
        self.trail_percentage = config["take_profit"]["trailing_percentage"]
        self.max_profit_percentage = config["take_profit"]["max_profit_percentage"]
        self.market_volatility_threshold = config["take_profit"]["volatility_threshold"]

    def calculate_dynamic_take_profit(self, trade_signal):
        """
        Calculates dynamic take-profit level based on market conditions.
        The algorithm uses trends, volatility, and other factors to adjust
        the take-profit level intelligently.
        """
        entry_price = trade_signal.get("entry_price", 0)
        market_condition = trade_signal.get("market_condition", "neutral")
        stop_loss_distance = trade_signal.get("stop_loss_distance", 0)
        volatility = self.get_market_volatility()

        # Apply a basic risk-reward ratio based on the stop-loss distance
        risk_reward_ratio = self.config["risk_management"]["risk_reward_ratio"]
        initial_take_profit = entry_price + (stop_loss_distance * risk_reward_ratio)

        # Adjust take-profit based on market trend (Trending Up, Trending Down, Neutral)
        if market_condition == "trending_up":
            take_profit = self.calculate_trending_up_take_profit(entry_price, stop_loss_distance)
        elif market_condition == "trending_down":
            take_profit = self.calculate_trending_down_take_profit(entry_price, stop_loss_distance)
        else:
            take_profit = initial_take_profit  # For neutral markets, use basic risk-reward approach

        # Apply trailing take-profit mechanism if market volatility is high
        if volatility > self.market_volatility_threshold:
            take_profit = self.apply_trailing_take_profit(take_profit, entry_price)

        # Prevent premature take-profit exits: cap the take-profit at a maximum limit
        take_profit = min(take_profit, entry_price * (1 + self.max_profit_percentage))

        return take_profit

    def calculate_trending_up_take_profit(self, entry_price, stop_loss_distance):
        """
        Calculates take-profit for a trending up market. The target is to capture more profit
        in strong trends.
        """
        trend_factor = 1.2  # Example factor for trending markets
        return entry_price + (stop_loss_distance * trend_factor)

    def calculate_trending_down_take_profit(self, entry_price, stop_loss_distance):
        """
        Calculates take-profit for a trending down market. The target is to exit early to prevent
        losses from worsening.
        """
        trend_factor = 0.8  # Example factor for downtrends (take-profit closer to entry)
        return entry_price - (stop_loss_distance * trend_factor)

    def get_market_volatility(self):
        """
        Returns market volatility. This could be calculated based on the standard deviation
        of price movements over a set period.
        """
        # For simplicity, mock volatility here. Replace with real calculation or external data.
        # Example: Get historical price data and calculate the volatility over the last X hours.
        volatility = np.random.uniform(0.05, 0.15)  # Example random volatility between 5% and 15%
        return volatility

    def apply_trailing_take_profit(self, take_profit, entry_price):
        """
        Applies a trailing take-profit based on the configured trailing percentage.
        This allows the take-profit level to "trail" the price as it moves in the trade's favor.
        """
        # Example trailing logic: take-profit trails the market by a percentage
        trailing_take_profit = entry_price * (1 + self.trail_percentage)
        return max(take_profit, trailing_take_profit)  # Ensure we don't lower the take-profit

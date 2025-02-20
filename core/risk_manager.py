import logging
import numpy as np

class RiskManager:
    """ AI-Driven Risk Management System """

    def __init__(self, max_risk_per_trade=0.02, min_stop_loss=0.005, max_stop_loss=0.03):
        """
        Initializes risk manager with dynamic risk control.

        :param max_risk_per_trade: Maximum % of balance risked per trade.
        :param min_stop_loss: Minimum stop-loss %.
        :param max_stop_loss: Maximum stop-loss %.
        """
        self.max_risk_per_trade = max_risk_per_trade
        self.min_stop_loss = min_stop_loss
        self.max_stop_loss = max_stop_loss

        # Setup logging
        logging.basicConfig(
            filename="logs/risk_manager.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def adjust_risk_based_on_sentiment(self, sentiment_score):
        """ Adjusts risk level based on AI sentiment analysis. """
        if sentiment_score < -0.3:  # Negative sentiment (High Risk)
            risk_multiplier = 0.5  # Reduce position size
        elif sentiment_score > 0.3:  # Positive sentiment (Low Risk)
            risk_multiplier = 1.2  # Increase position size slightly
        else:
            risk_multiplier = 1.0  # Normal risk

        adjusted_risk = max(self.max_risk_per_trade * risk_multiplier, 0.01)
        logging.info("Adjusted risk level: %.4f based on sentiment score %.2f", adjusted_risk, sentiment_score)
        return adjusted_risk

    def calculate_position_size(self, balance, trade_risk, sentiment_score):
        """ Calculates optimal position size with AI-based risk management. """
        adjusted_risk = self.adjust_risk_based_on_sentiment(sentiment_score)
        position_size = (balance * adjusted_risk) / trade_risk

        logging.info("Position size: %.2f units with risk: %.4f", position_size, adjusted_risk)
        return max(position_size, 1)  

    def determine_stop_loss(self, volatility, sentiment_score):
        """ Determines stop-loss dynamically based on market conditions. """
        if sentiment_score < -0.3:  # Negative sentiment
            stop_loss = self.max_stop_loss  # Wider stop to avoid market noise
        elif sentiment_score > 0.3:  # Positive sentiment
            stop_loss = self.min_stop_loss  # Tighter stop for quick profit-taking
        else:
            stop_loss = np.clip(volatility * 0.02, self.min_stop_loss, self.max_stop_loss)

        logging.info("AI Stop-Loss set at %.4f", stop_loss)
        return stop_loss

# Example Usage
if __name__ == "__main__":
    risk_manager = RiskManager()

    sentiment = -0.4  # Negative Sentiment
    balance = 10000
    trade_risk = 500
    volatility = 0.015

    position_size = risk_manager.calculate_position_size(balance, trade_risk, sentiment)
    stop_loss = risk_manager.determine_stop_loss(volatility, sentiment)

    print("AI-Adjusted Position Size:", position_size)
    print("AI-Adjusted Stop-Loss:", stop_loss)

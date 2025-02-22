import logging
from technical_indicators import TechnicalIndicators
from sentiment_analysis import SentimentAnalyzer
from market_conditions import MarketConditions

class AITradeExplanation:
    """ AI-driven trade explanation system for understanding trade decisions """
    
    def __init__(self, config):
        """
        Initializes the AI Trade Explanation module.
        :param config: Configuration dictionary.
        """
        self.config = config
        self.technical_indicators = TechnicalIndicators(config)
        self.sentiment_analyzer = SentimentAnalyzer(config)
        self.market_conditions = MarketConditions(config)
        
        # Setup logging
        logging.basicConfig(
            filename="logs/ai_trade_explanation.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def generate_explanation(self, trade_signal):
        """
        Generates a human-readable explanation for a given trade signal.
        :param trade_signal: Dictionary containing trade signal details.
        :return: String explanation of the trade decision.
        """
        symbol = trade_signal["symbol"]
        action = trade_signal["action"]
        rationale = []

        # Step 1: Add explanation based on technical indicators
        technical_explanation = self._explain_technical_indicators(symbol, action)
        rationale.append(f"Technical Indicators: {technical_explanation}")

        # Step 2: Add sentiment analysis explanation
        sentiment_explanation = self._explain_sentiment(symbol)
        rationale.append(f"Sentiment Analysis: {sentiment_explanation}")

        # Step 3: Add market conditions explanation
        market_condition_explanation = self._explain_market_conditions(symbol)
        rationale.append(f"Market Conditions: {market_condition_explanation}")

        # Combine all explanations into a final one
        final_explanation = "\n".join(rationale)
        return final_explanation

    def _explain_technical_indicators(self, symbol, action):
        """
        Provide an explanation based on the technical indicators like RSI, MACD, etc.
        :param symbol: Trading asset symbol.
        :param action: Action to be taken (Buy/Sell/Hold).
        :return: String explanation for technical indicators.
        """
        rsi = self.technical_indicators.get_rsi(symbol)
        macd = self.technical_indicators.get_macd(symbol)
        moving_avg = self.technical_indicators.get_moving_average(symbol, window=50)

        explanation = f"RSI is {rsi:.2f}, MACD is {macd:.2f}, and 50-day MA is {moving_avg:.2f}. "
        
        if action == "Buy":
            if rsi < 30 and macd > 0 and moving_avg > self.technical_indicators.get_latest_price(symbol):
                explanation += "The RSI indicates oversold conditions, MACD is positive, and the price is above the 50-day moving average, making a Buy signal strong."
            elif rsi < 40 and macd > 0:
                explanation += "The RSI is low, but MACD is positive, indicating a potential Buy signal."
            else:
                explanation += "Technical indicators do not strongly favor a Buy signal."
        elif action == "Sell":
            if rsi > 70 and macd < 0 and moving_avg < self.technical_indicators.get_latest_price(symbol):
                explanation += "RSI is overbought, MACD is negative, and price is below the 50-day moving average, signaling a strong Sell."
            elif rsi > 60 and macd < 0:
                explanation += "RSI is high, and MACD is negative, suggesting a Sell signal."
            else:
                explanation += "Technical indicators do not strongly favor a Sell signal."
        else:  # Hold
            explanation += "The indicators do not suggest a strong Buy or Sell, so we recommend holding the position."
        
        return explanation

    def _explain_sentiment(self, symbol):
        """
        Provide an explanation based on sentiment analysis of news, social media, etc.
        :param symbol: Trading asset symbol.
        :return: String explanation for sentiment.
        """
        sentiment_score = self.sentiment_analyzer.analyze_sentiment(symbol)
        if sentiment_score > 0.7:
            return f"Sentiment analysis shows strong positive sentiment towards {symbol}, suggesting a potential Buy."
        elif sentiment_score < 0.3:
            return f"Sentiment analysis shows strong negative sentiment towards {symbol}, suggesting a potential Sell."
        else:
            return f"Sentiment analysis shows neutral sentiment towards {symbol}, which supports a Hold decision."

    def _explain_market_conditions(self, symbol):
        """
        Provide an explanation based on current market conditions.
        :param symbol: Trading asset symbol.
        :return: String explanation for market conditions.
        """
        trend_strength = self.market_conditions.get_trend_strength(symbol)
        volatility = self.market_conditions.get_volatility(symbol)
        
        if trend_strength > 0.7:
            trend_message = "The market trend is strong."
        elif trend_strength < 0.3:
            trend_message = "The market trend is weak."
        else:
            trend_message = "The market trend is neutral."

        if volatility > 0.02:
            volatility_message = "The market is experiencing high volatility."
        else:
            volatility_message = "The market is stable with low volatility."
        
        return f"{trend_message} {volatility_message}"


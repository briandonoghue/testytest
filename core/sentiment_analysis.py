import logging
import requests
from textblob import TextBlob
from news_scraper import NewsScraper
from social_media_scraper import SocialMediaScraper
from config_loader import ConfigLoader

class SentimentAnalyzer:
    """
    SentimentAnalyzer is responsible for analyzing market sentiment from news articles, social media, 
    and other text-based sources to gauge the mood of the market around a specific asset.
    """
    
    def __init__(self, config):
        """
        Initializes the SentimentAnalyzer class with configuration settings.
        :param config: Configuration dictionary containing settings for sentiment analysis.
        """
        self.config = config
        self.news_scraper = NewsScraper(config)
        self.social_media_scraper = SocialMediaScraper(config)

        # Logging setup
        logging.basicConfig(
            filename="logs/sentiment_analyzer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
    
    def analyze_sentiment(self, symbol):
        """
        Analyzes sentiment for a given asset symbol based on news articles and social media posts.
        :param symbol: Trading asset symbol (e.g., 'AAPL', 'BTC/USD', etc.).
        :return: Sentiment score ranging from -1 (negative) to 1 (positive).
        """
        logging.info(f"Analyzing sentiment for {symbol}...")

        # Fetch news articles and social media posts related to the asset symbol
        news_data = self.news_scraper.fetch_news(symbol)
        social_media_data = self.social_media_scraper.fetch_social_media_posts(symbol)

        if not news_data and not social_media_data:
            logging.warning(f"No sentiment data available for {symbol}.")
            return 0  # Neutral sentiment if no data is found

        # Combine all text sources for sentiment analysis
        all_text_data = []
        if news_data:
            all_text_data.extend(news_data)
        if social_media_data:
            all_text_data.extend(social_media_data)

        # Calculate sentiment score using TextBlob
        sentiment_score = self._calculate_sentiment(all_text_data)

        logging.info(f"Sentiment score for {symbol}: {sentiment_score}")
        return sentiment_score
    
    def _calculate_sentiment(self, text_data):
        """
        Calculates sentiment based on the aggregated text data from news and social media.
        Uses TextBlob for basic sentiment analysis.
        :param text_data: List of text data (news articles, social media posts, etc.).
        :return: Sentiment score between -1 (negative) and 1 (positive).
        """
        total_sentiment = 0
        num_texts = len(text_data)

        for text in text_data:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity  # Sentiment polarity (-1 to 1)
            total_sentiment += sentiment

        # Normalize the sentiment score
        average_sentiment = total_sentiment / num_texts if num_texts > 0 else 0
        return round(average_sentiment, 2)


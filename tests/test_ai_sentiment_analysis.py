import unittest
import json
from core.ai_sentiment_analysis import AISentimentAnalyzer

class TestAISentimentAnalysis(unittest.TestCase):
    """ Unit tests for AI-powered market sentiment analysis """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize AISentimentAnalyzer """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.sentiment_analyzer = AISentimentAnalyzer(cls.config)

    def test_news_sentiment_analysis(self):
        """ Ensure AI correctly analyzes financial news sentiment """
        news_data = [
            "Bitcoin hits new all-time high as investors pile in.",
            "Stock market crash fears grow amid rising inflation."
        ]

        sentiment_score = self.sentiment_analyzer.analyze_news_sentiment(news_data)

        self.assertIsInstance(sentiment_score, float, "Sentiment score should be a float value")
        self.assertGreaterEqual(sentiment_score, -1, "Sentiment score should be within valid range (-1 to 1)")
        self.assertLessEqual(sentiment_score, 1, "Sentiment score should be within valid range (-1 to 1)")

    def test_social_media_sentiment(self):
        """ Validate AI processes social media sentiment accurately """
        social_posts = [
            "Ethereum is mooning! 🚀🚀 #crypto",
            "Markets are crashing! Time to panic?"
        ]

        sentiment_score = self.sentiment_analyzer.analyze_social_media_sentiment(social_posts)

        self.assertIsInstance(sentiment_score, float, "Sentiment score should be a float value")
        self.assertGreaterEqual(sentiment_score, -1, "Sentiment score should be within valid range (-1 to 1)")
        self.assertLessEqual(sentiment_score, 1, "Sentiment score should be within valid range (-1 to 1)")

    def test_economic_indicator_sentiment(self):
        """ Ensure AI integrates economic indicators into sentiment analysis """
        economic_data = {
            "interest_rate_change": -0.25,
            "CPI_inflation": 3.5,
            "GDP_growth": 2.1
        }

        sentiment_adjustment = self.sentiment_analyzer.analyze_economic_indicators(economic_data)

        self.assertIsInstance(sentiment_adjustment, float, "Economic sentiment adjustment should be a float value")
        self.assertGreaterEqual(sentiment_adjustment, -1, "Economic sentiment score should be within valid range (-1 to 1)")
        self.assertLessEqual(sentiment_adjustment, 1, "Economic sentiment score should be within valid range (-1 to 1)")

    def test_combined_sentiment_analysis(self):
        """ Validate AI integrates multiple sentiment sources into a final score """
        sentiment_data = {
            "news_sentiment": 0.3,
            "social_media_sentiment": -0.2,
            "economic_sentiment": 0.1
        }

        final_sentiment_score = self.sentiment_analyzer.compute_combined_sentiment(sentiment_data)

        self.assertIsInstance(final_sentiment_score, float, "Final sentiment score should be a float value")
        self.assertGreaterEqual(final_sentiment_score, -1, "Final sentiment score should be within valid range (-1 to 1)")
        self.assertLessEqual(final_sentiment_score, 1, "Final sentiment score should be within valid range (-1 to 1)")

    def test_sentiment_log_integration(self):
        """ Ensure AI logs sentiment analysis results for tracking """
        sentiment_log_entry = {
            "symbol": "BTCUSDT",
            "sentiment_score": 0.6,
            "source": "news",
            "timestamp": "2025-02-20 20:30:00"
        }

        log_result = self.sentiment_analyzer.log_sentiment_analysis(sentiment_log_entry)

        self.assertTrue(log_result, "AI should successfully log sentiment analysis results")

if __name__ == "__main__":
    unittest.main()

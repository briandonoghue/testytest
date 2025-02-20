import unittest
from unittest.mock import patch
from ml.sentiment_analyzer import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):
    """ Unit tests for AI Sentiment Analyzer """

    def setUp(self):
        """ Initializes SentimentAnalyzer instance. """
        self.sentiment_analyzer = SentimentAnalyzer()

    @patch("ml.sentiment_analyzer.requests.get")
    def test_fetch_news_headlines(self, mock_get):
        """ Tests successful retrieval of financial news headlines. """
        mock_html = """
        <html>
            <body>
                <h2>Gold prices surge due to inflation fears</h2>
                <h3>Stock market struggles amid interest rate concerns</h3>
            </body>
        </html>
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_html

        headlines = self.sentiment_analyzer.fetch_news_headlines()
        self.assertGreater(len(headlines), 0)
        self.assertIn("Gold prices surge due to inflation fears", headlines)

    @patch("ml.sentiment_analyzer.pipeline")
    def test_analyze_sentiment(self, mock_pipeline):
        """ Tests sentiment analysis classification accuracy. """
        mock_pipeline.return_value = lambda text: [{"label": "POSITIVE", "score": 0.85}]

        sentiment = self.sentiment_analyzer.analyze_sentiment()
        self.assertEqual(sentiment["Sentiment"], "Positive")
        self.assertGreater(sentiment["Score"], 0.2)

    @patch("ml.sentiment_analyzer.pipeline")
    def test_analyze_negative_sentiment(self, mock_pipeline):
        """ Tests negative sentiment classification. """
        mock_pipeline.return_value = lambda text: [{"label": "NEGATIVE", "score": 0.9}]

        sentiment = self.sentiment_analyzer.analyze_sentiment()
        self.assertEqual(sentiment["Sentiment"], "Negative")
        self.assertLess(sentiment["Score"], -0.2)

    def test_handle_no_headlines(self):
        """ Ensures AI handles cases where no news headlines are available. """
        self.sentiment_analyzer.fetch_news_headlines = lambda: []
        sentiment = self.sentiment_analyzer.analyze_sentiment()

        self.assertEqual(sentiment["Sentiment"], "Neutral")
        self.assertEqual(sentiment["Score"], 0.0)

if __name__ == "__main__":
    unittest.main()

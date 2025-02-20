import logging
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

class SentimentAnalyzer:
    """ Fetches financial news and performs sentiment analysis. """

    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis")
        self.news_sources = [
            "https://www.reuters.com/markets",
            "https://www.cnbc.com/markets",
            "https://www.bloomberg.com/markets"
        ]

        # Setup logging
        logging.basicConfig(
            filename="logs/sentiment_analyzer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def fetch_news_headlines(self):
        """ Scrapes latest financial news headlines from sources. """
        headlines = []
        try:
            for url in self.news_sources:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                
                for tag in soup.find_all(["h2", "h3"]):
                    if tag.text and len(tag.text) > 10:
                        headlines.append(tag.text.strip())

            logging.info("Fetched %d news headlines.", len(headlines))
            return headlines[:10]  # Return the latest 10 headlines

        except Exception as e:
            logging.error("Failed to fetch news: %s", e)
            return []

    def analyze_sentiment(self):
        """ Analyzes sentiment of financial news headlines. """
        headlines = self.fetch_news_headlines()
        if not headlines:
            return {"Sentiment": "Neutral", "Score": 0.0}

        sentiment_results = self.sentiment_pipeline(headlines)
        avg_score = sum([res["score"] if res["label"] == "POSITIVE" else -res["score"] for res in sentiment_results]) / len(sentiment_results)

        sentiment = "Positive" if avg_score > 0.2 else "Negative" if avg_score < -0.2 else "Neutral"
        logging.info("News Sentiment: %s (Score: %.2f)", sentiment, avg_score)

        return {"Sentiment": sentiment, "Score": avg_score}

# Example Usage
if __name__ == "__main__":
    sentiment_analyzer = SentimentAnalyzer()
    sentiment = sentiment_analyzer.analyze_sentiment()
    print("Market Sentiment:", sentiment)

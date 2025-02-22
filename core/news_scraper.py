import logging
import numpy as np
import requests
from bs4 import BeautifulSoup

class NewsScraper:
    """
    NewsScraper class is responsible for scraping and collecting news articles from a given source.
    It can fetch articles related to market events, economic news, and company-specific updates.
    """

    def __init__(self, config):
        """
        Initializes the NewsScraper class with configuration settings.
        :param config: Configuration dictionary containing news scraping settings.
        """
        self.config = config
        self.news_api_url = config["news_api"]["news_api_url"]
        self.api_key = config["news_api"]["api_key"]
        
        # Logging setup
        logging.basicConfig(
            filename="logs/news_scraper.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def fetch_news_from_api(self, query):
        """
        Fetches news articles related to a query from the news API.
        :param query: The search query string to fetch relevant news articles.
        :return: List of articles with titles, descriptions, and URLs.
        """
        url = f"{self.news_api_url}?q={query}&apiKey={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json().get("articles", [])
            if articles:
                logging.info(f"Fetched {len(articles)} articles for query '{query}'.")
            else:
                logging.warning(f"No articles found for query '{query}'.")
            return articles
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching news from API: {e}")
            return []

    def scrape_news_from_website(self, url):
        """
        Scrapes news articles directly from a website using BeautifulSoup.
        :param url: The URL of the website to scrape.
        :return: List of articles with titles, descriptions, and URLs.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            articles = self.extract_articles_from_html(soup)
            logging.info(f"Scraped {len(articles)} articles from website: {url}.")
            return articles
        except requests.exceptions.RequestException as e:
            logging.error(f"Error scraping news from website: {e}")
            return []

    def extract_articles_from_html(self, soup):
        """
        Extracts news articles from a BeautifulSoup HTML object.
        This can be customized for different websites' structures.
        :param soup: BeautifulSoup object containing the website's HTML.
        :return: List of articles with titles, descriptions, and URLs.
        """
        articles = []
        for article_tag in soup.find_all("article"):
            title_tag = article_tag.find("h2")
            description_tag = article_tag.find("p")
            link_tag = article_tag.find("a")
            
            if title_tag and description_tag and link_tag:
                title = title_tag.get_text(strip=True)
                description = description_tag.get_text(strip=True)
                link = link_tag.get("href")
                if link:
                    articles.append({
                        "title": title,
                        "description": description,
                        "url": link
                    })
        return articles

    def get_recent_market_news(self):
        """
        Retrieves the most recent market news using either the API or scraping.
        :return: List of the most recent market news articles.
        """
        query = "market news"  # You can customize the query to target specific topics like "stocks" or "commodities"
        articles_from_api = self.fetch_news_from_api(query)

        if not articles_from_api:
            # If API fails or returns no articles, fall back to web scraping
            logging.info("Falling back to website scraping for market news.")
            url = "https://www.example-news-site.com/market-news"  # Placeholder URL
            articles_from_web = self.scrape_news_from_website(url)
            return articles_from_web
        
        return articles_from_api

    def get_article_sentiment(self, article):
        """
        Analyzes the sentiment of a news article based on its title or content.
        You could integrate an external sentiment analysis API or library here.
        :param article: Dictionary containing article title and description.
        :return: Sentiment score (e.g., -1 = negative, 0 = neutral, 1 = positive).
        """
        # Example placeholder sentiment analysis based on keywords
        positive_keywords = ["positive", "increase", "growth", "up", "surge"]
        negative_keywords = ["negative", "decrease", "fall", "down", "drop"]
        
        text = f"{article['title']} {article['description']}"
        
        score = 0
        for word in positive_keywords:
            if word.lower() in text.lower():
                score += 1
        for word in negative_keywords:
            if word.lower() in text.lower():
                score -= 1
                
        # Normalize score to be between -1 and 1
        sentiment_score = np.clip(score / len(positive_keywords), -1, 1)
        return sentiment_score

    def save_articles(self, articles):
        """
        Saves the fetched articles into a file or database for later analysis.
        :param articles: List of articles to save.
        """
        with open("scraped_articles.json", "w") as file:
            json.dump(articles, file, indent=4)
            logging.info(f"Saved {len(articles)} articles to 'scraped_articles.json'.")

    def display_news(self, articles):
        """
        Displays the fetched articles in a simple readable format.
        :param articles: List of articles to display.
        """
        for article in articles:
            print(f"Title: {article['title']}")
            print(f"Description: {article['description']}")
            print(f"URL: {article['url']}\n")

# Example usage:
if __name__ == "__main__":
    # Load config (assuming configuration is in place)
    config = {
        "news_api_url": "https://newsapi.org/v2/everything",
        "api_key": "your-api-key-here"
    }
    scraper = NewsScraper(config)
    
    # Fetch and display recent market news
    market_news = scraper.get_recent_market_news()
    scraper.display_news(market_news)

    # Save the news to a file
    scraper.save_articles(market_news)

import logging
import requests
import tweepy
from psaw import PushshiftAPI  # For Reddit scraping
import json

class SocialMediaScraper:
    """
    SocialMediaScraper is responsible for scraping relevant market sentiment from social media platforms like
    Twitter and Reddit. This information is useful to assess public sentiment, which can impact market trends.
    """

    def __init__(self, config):
        """
        Initializes the SocialMediaScraper with API keys and configuration settings.
        :param config: Configuration dictionary containing social media API credentials and settings.
        """
        self.config = config
        self.twitter_api_key = config["settings"]["twitter"]["twitter_api_key"]
        self.twitter_api_secret = config["settings"]["twitter"]["twitter_api_secret"]
        self.twitter_access_token = config["settings"]["twitter"]["twitter_access_token"]
        self.twitter_access_token_secret = config["settings"]["twitter"]["twitter_access_token_secret"]
        self.reddit_client_id = config["settings"]["reddit"]["reddit_client_id"]
        self.reddit_client_secret = config["settings"]["reddit"]["reddit_client_secret"]
        self.reddit_user_agent = config["settings"]["reddit"]["reddit_user_agent"]

        # Setup logging
        logging.basicConfig(
            filename="logs/social_media_scraper.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # Initialize Twitter API client
        self.twitter_auth = tweepy.OAuth1UserHandler(
            consumer_key=self.twitter_api_key,
            consumer_secret=self.twitter_api_secret,
            access_token=self.twitter_access_token,
            access_token_secret=self.twitter_access_token_secret
        )
        self.twitter_api = tweepy.API(self.twitter_auth)

        # Initialize Reddit API client
        #self.reddit_api = PushshiftAPI()

    def fetch_twitter_posts(self, hashtag, count=100):
        """
        Fetches tweets from Twitter based on a hashtag.
        :param hashtag: The hashtag to search for.
        :param count: The number of tweets to fetch.
        :return: List of tweet texts.
        """
        try:
            tweets = tweepy.Cursor(self.twitter_api.search,
                                   q=hashtag,
                                   lang="en",
                                   tweet_mode="extended").items(count)
            tweet_texts = [tweet.full_text for tweet in tweets]
            logging.info(f"Fetched {len(tweet_texts)} tweets with hashtag {hashtag}.")
            return tweet_texts
        except tweepy.TweepError as e:
            logging.error(f"Error fetching tweets: {e}")
            return []

    def fetch_reddit_posts(self, subreddit, keyword, count=100):
        """
        Fetches posts from Reddit based on a subreddit and keyword.
        :param subreddit: The subreddit to search.
        :param keyword: The keyword to search for in the posts.
        :param count: The number of posts to fetch.
        :return: List of post texts.
        """
        try:
            submissions = self.reddit_api.search_submissions(
                q=keyword,
                subreddits=[subreddit],
                limit=count
            )
            post_texts = [submission.title + " " + submission.selftext for submission in submissions]
            logging.info(f"Fetched {len(post_texts)} posts from subreddit {subreddit} with keyword {keyword}.")
            return post_texts
        except Exception as e:
            logging.error(f"Error fetching Reddit posts: {e}")
            return []

    def analyze_sentiment(self, text):
        """
        Analyzes the sentiment of the given text (simple positive/negative classification).
        :param text: The text to analyze.
        :return: Sentiment score (-1 for negative, 0 for neutral, 1 for positive).
        """
        # Simple sentiment analysis: example implementation with keyword-based analysis
        positive_keywords = ["good", "positive", "up", "surge", "gain", "increase"]
        negative_keywords = ["bad", "negative", "down", "decline", "loss", "decrease"]

        score = 0
        for word in positive_keywords:
            if word.lower() in text.lower():
                score += 1
        for word in negative_keywords:
            if word.lower() in text.lower():
                score -= 1

        sentiment_score = 0
        if score > 0:
            sentiment_score = 1
        elif score < 0:
            sentiment_score = -1
        else:
            sentiment_score = 0

        return sentiment_score

    def aggregate_sentiment(self, texts):
        """
        Aggregates sentiment of a list of social media posts.
        :param texts: List of texts from social media posts.
        :return: Aggregated sentiment score for the posts.
        """
        sentiment_scores = [self.analyze_sentiment(text) for text in texts]
        aggregated_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        return aggregated_sentiment

    def get_market_sentiment(self, hashtag, subreddit, keyword):
        """
        Gets aggregated market sentiment from social media sources like Twitter and Reddit.
        :param hashtag: The hashtag to search for on Twitter.
        :param subreddit: The subreddit to search for on Reddit.
        :param keyword: The keyword to search for in Reddit posts.
        :return: Aggregated sentiment score from both sources.
        """
        twitter_posts = self.fetch_twitter_posts(hashtag)
        reddit_posts = self.fetch_reddit_posts(subreddit, keyword)

        twitter_sentiment = self.aggregate_sentiment(twitter_posts)
        reddit_sentiment = self.aggregate_sentiment(reddit_posts)

        aggregated_sentiment = (twitter_sentiment + reddit_sentiment) / 2

        logging.info(f"Aggregated Market Sentiment: {aggregated_sentiment}")
        return aggregated_sentiment

    def save_social_media_data(self, twitter_posts, reddit_posts):
        """
        Saves the fetched social media data into a file or database for later analysis.
        :param twitter_posts: List of tweets.
        :param reddit_posts: List of Reddit posts.
        """
        data = {
            "twitter_posts": twitter_posts,
            "reddit_posts": reddit_posts
        }
        with open("social_media_data.json", "w") as f:
            json.dump(data, f)
        logging.info("Social media data saved successfully.")

    def run(self, hashtag, subreddit, keyword):
        """
        Runs the social media scraper to fetch, analyze, and save social media posts.
        :param hashtag: The hashtag to search for on Twitter.
        :param subreddit: The subreddit to search for on Reddit.
        :param keyword: The keyword to search for in Reddit posts.
        """
        twitter_posts = self.fetch_twitter_posts(hashtag)
        reddit_posts = self.fetch_reddit_posts(subreddit, keyword)

        aggregated_sentiment = self.get_market_sentiment(hashtag, subreddit, keyword)

        self.save_social_media_data(twitter_posts, reddit_posts)

        logging.info(f"Sentiment Analysis Complete. Aggregated Sentiment: {aggregated_sentiment}")

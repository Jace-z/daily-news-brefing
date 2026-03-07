import feedparser
import requests
import json
import os
from typing import List, Dict

class NewsFetcher:
    """
    Fetches news from various sources including RSS feeds and News APIs.
    """

    def __init__(self, news_api_key: str = None):
        self.news_api_key = news_api_key

    def fetch_rss_feed(self, url: str) -> List[Dict]:
        """
        Fetches and parses an RSS feed.
        """
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            articles.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'summary': entry.get('summary', ''),
                'published': entry.get('published', ''),
                'source': feed.feed.get('title', 'Unknown RSS Source')
            })
        return articles

    def fetch_news_api(self, query: str, language: str = 'en') -> List[Dict]:
        """
        Fetches news from NewsAPI.org.
        """
        if not self.news_api_key:
            return []

        url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={self.news_api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return []

        data = response.json()
        articles = []
        for article in data.get('articles', []):
            articles.append({
                'title': article.get('title', ''),
                'link': article.get('url', ''),
                'summary': article.get('description', ''),
                'published': article.get('publishedAt', ''),
                'source': article.get('source', {}).get('name', 'NewsAPI')
            })
        return articles

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test RSS fetching
    fetcher = NewsFetcher(news_api_key=os.getenv("NEWS_API_KEY"))
    rss_articles = fetcher.fetch_rss_feed("https://feeds.bbci.co.uk/news/rss.xml")
    print(f"Fetched {len(rss_articles)} articles from BBC RSS.")
    for art in rss_articles[:3]:
        print(f"- {art['title']}")
        
    # Test NewsAPI fetching
    if fetcher.news_api_key:
        print("\nTesting NewsAPI with query 'AI'...")
        api_articles = fetcher.fetch_news_api("AI")
        print(f"Fetched {len(api_articles)} articles from NewsAPI.")
        for art in api_articles[:3]:
            print(f"- {art['title']} (Source: {art['source']})")
    else:
        print("\nNo NEWS_API_KEY found in .env, skipping NewsAPI test.")

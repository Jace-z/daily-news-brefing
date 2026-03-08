import feedparser
import requests
import json
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta, timezone
import time

class NewsFetcher:
    """
    Fetches news from various sources including RSS feeds and News APIs.
    Filters by timeframe and performs deduplication.
    """

    def __init__(self, news_api_key: str = None):
        self.news_api_key = news_api_key

    def fetch_rss_feed(self, url: str, since: datetime) -> List[Dict]:
        """
        Fetches and parses an RSS feed, filtering for articles published after 'since'.
        """
        feed = feedparser.parse(url)
        articles = []
        
        for entry in feed.entries:
            published_time = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc)
            
            if published_time and published_time < since:
                continue

            articles.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'summary': entry.get('summary', ''),
                'published': published_time.isoformat() if published_time else entry.get('published', ''),
                'source': feed.feed.get('title', 'Unknown RSS Source')
            })
        return articles

    def fetch_top_headlines(self, country: str = 'us', category: str = None) -> List[Dict]:
        """
        Fetches the latest top headlines from NewsAPI.
        """
        if not self.news_api_key:
            return []

        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={self.news_api_key}"
        if category:
            url += f"&category={category}"

        try:
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
        except Exception as e:
            print(f"Error fetching top headlines: {e}")
            return []

    def fetch_news_api(self, query: str, since: datetime, language: str = 'en', max_results: int = 15) -> List[Dict]:
        """
        Fetches news from NewsAPI.org 'everything' endpoint.
        """
        if not self.news_api_key:
            return []

        # Ensure correct ISO format for NewsAPI (no microseconds/timezone offset suffix)
        from_param = since.strftime('%Y-%m-%dT%H:%M:%S')
        
        url = (
            f"https://newsapi.org/v2/everything?q={query}"
            f"&from={from_param}"
            f"&language={language}"
            f"&sortBy=relevancy"
            f"&pageSize={max_results}"
            f"&apiKey={self.news_api_key}"
        )
        print(f"DEBUG: Calling NewsAPI: {url.replace(self.news_api_key, 'HIDDEN')}")
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"NewsAPI Everything Error: {response.status_code}")
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
        except Exception as e:
            print(f"Error calling NewsAPI Everything: {e}")
            return []

    @staticmethod
    def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
        """
        Removes duplicate articles based on normalized title or URL.
        """
        seen_links = set()
        seen_titles = set()
        unique_articles = []

        for article in articles:
            link = article.get('link')
            title = article.get('title', '').strip().lower()
            
            if not title:
                continue

            if link not in seen_links and title not in seen_titles:
                seen_links.add(link)
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Correct 24h window in UTC
    since_24h = datetime.now(timezone.utc) - timedelta(hours=24)
    fetcher = NewsFetcher(news_api_key=os.getenv("NEWS_API_KEY"))
    
    print(f"--- Fetching News (Since UTC: {since_24h.strftime('%Y-%m-%d %H:%M:%S')}) ---")
    
    # 1. Test RSS
    rss = fetcher.fetch_rss_feed("https://feeds.bbci.co.uk/news/rss.xml", since=since_24h)
    print(f"RSS (BBC): {len(rss)} articles")
    
    # 2. Test Everything (Query)
    api_ev = fetcher.fetch_news_api("Economy", since=since_24h)
    print(f"NewsAPI Everything (Economy): {len(api_ev)} articles")
    
    # 3. Test Top Headlines
    api_top = fetcher.fetch_top_headlines(country='us')
    print(f"NewsAPI Top Headlines: {len(api_top)} articles")
    
    combined = rss + api_ev + api_top
    deduped = fetcher.deduplicate_articles(combined)
    print(f"Total: {len(combined)}, Unique: {len(deduped)}")
    
    for art in deduped[:5]:
        print(f"- {art['title']} ({art['source']})")

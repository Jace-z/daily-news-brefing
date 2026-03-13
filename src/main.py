import os
import json
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from news_fetcher import NewsFetcher
from gemini_summarizer import GeminiSummarizer
from infrastructure.db_factory import get_db_client
from email_distributor import EmailDistributor
from email_formatter import format_as_html
from google.cloud import secretmanager

# Load local environment variables if present
load_dotenv()

def get_secret(secret_id: str, project_id: str) -> str:
    """
    Retrieves a secret from GCP Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def main():
    # Configuration
    PROJECT_ID = os.getenv("PROJECT_ID")
    LOCATION = os.getenv("LOCATION", "australia-southeast1")
    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "resend")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    
    USE_SECRET_MANAGER = os.getenv("USE_SECRET_MANAGER", "false").lower() == "true"
    
    if USE_SECRET_MANAGER:
        NEWS_API_KEY = get_secret("NEWS_API_KEY", PROJECT_ID)
        EMAIL_API_KEY = get_secret("EMAIL_API_KEY", PROJECT_ID)
    else:
        NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

    # Initialize Clients
    fetcher = NewsFetcher(news_api_key=NEWS_API_KEY)
    summarizer = GeminiSummarizer(project_id=PROJECT_ID)
    db = get_db_client(project_id=PROJECT_ID)
    distributor = EmailDistributor(api_key=EMAIL_API_KEY, sender_email=SENDER_EMAIL, provider=EMAIL_PROVIDER)

    # 1. Fetch User Profiles
    profiles = db.get_user_profiles()
    print(f"Processing {len(profiles)} user profiles.")

    for profile in profiles:
        user_id = profile['id']
        email = profile['email']
        interests = profile.get('interests', [])
        rss_feeds = profile.get('rss_feeds', [])
        last_sent = profile.get('last_sent')

        # Calculate time window (48h min)
        now_utc = datetime.now(timezone.utc)
        if last_sent:
            since = last_sent.replace(tzinfo=timezone.utc) if last_sent.tzinfo is None else last_sent
            min_window = now_utc - timedelta(hours=48)
            if since > min_window:
                since = min_window
        else:
            since = now_utc - timedelta(hours=48)
        
        print(f"Processing briefing for: {email}")

        # 2. Fetch and Summarize BY INTEREST
        briefing_data = []
        
        # RSS Section
        if rss_feeds:
            all_rss_articles = []
            for url in rss_feeds:
                all_rss_articles.extend(fetcher.fetch_rss_feed(url, since=since))
            
            if all_rss_articles:
                print(f"Summarizing RSS feeds...")
                rss_summary = summarizer.summarize_articles(all_rss_articles, user_interests=["General News"])
                briefing_data.append({"interest": "Latest Headlines", "content": rss_summary})

        # Interest Sections
        for interest in interests:
            print(f"Fetching news for interest: {interest}...")
            interest_articles = fetcher.fetch_news_api(interest, since=since)
            
            if interest_articles:
                print(f"Summarizing interest: {interest}...")
                interest_summary = summarizer.summarize_articles(interest_articles, user_interests=[interest])
                briefing_data.append({"interest": interest, "content": interest_summary})

        if not briefing_data:
            print(f"No new news for {email} today.")
            continue

        # 3. Format using local Python Template
        html_content = format_as_html(briefing_data)

        # 4. Distribute via Email
        date_str = datetime.now().strftime("%B %d, %Y")
        subject = f"Your Daily News Briefing - {date_str}"
        success = distributor.send_briefing(email, subject, html_content)

        if success:
            print(f"Successfully sent briefing to {email}")
            db.update_last_sent(user_id)
        else:
            print(f"Failed to send briefing to {email}")

if __name__ == "__main__":
    main()

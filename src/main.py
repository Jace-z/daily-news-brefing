import os
import json
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from news_fetcher import NewsFetcher
from gemini_summarizer import GeminiSummarizer
from firestore_client import FirestoreClient
from email_distributor import EmailDistributor
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
    LOCATION = os.getenv("LOCATION", "global")
    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "resend")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    
    # In production, we might fetch these from Secret Manager
    USE_SECRET_MANAGER = os.getenv("USE_SECRET_MANAGER", "false").lower() == "true"
    
    if USE_SECRET_MANAGER:
        NEWS_API_KEY = get_secret("NEWS_API_KEY", PROJECT_ID)
        EMAIL_API_KEY = get_secret("EMAIL_API_KEY", PROJECT_ID)
    else:
        NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

    # Initialize Clients
    fetcher = NewsFetcher(news_api_key=NEWS_API_KEY)
    summarizer = GeminiSummarizer(project_id=PROJECT_ID, location=LOCATION)
    db = FirestoreClient(project_id=PROJECT_ID)
    distributor = EmailDistributor(api_key=EMAIL_API_KEY, sender_email=SENDER_EMAIL, provider=EMAIL_PROVIDER)

    # 1. Fetch User Profiles
    profiles = db.get_user_profiles()
    print(f"Processing {len(profiles)} user profiles.")

    for profile in profiles:
        user_id = profile['id']
        email = profile['email']
        interests = profile.get('interests', [])
        rss_feeds = profile.get('rss_feeds', [])
        last_sent = profile.get('last_sent') # Firestore timestamp

        # Calculate time window (since last sent, with a minimum of 48 hours for reliability)
        now_utc = datetime.now(timezone.utc)
        if last_sent:
            since = last_sent.replace(tzinfo=timezone.utc) if last_sent.tzinfo is None else last_sent
            # Ensure at least 48 hours buffer if last_sent was very recent
            min_window = now_utc - timedelta(hours=48)
            if since > min_window:
                since = min_window
        else:
            since = now_utc - timedelta(hours=48)
        
        print(f"Processing briefing for: {email} (fetching news since: {since.isoformat()})")

        # 2. Fetch News
        all_articles = []
        for feed_url in rss_feeds:
            all_articles.extend(fetcher.fetch_rss_feed(feed_url, since=since))
        
        # Fetch from NewsAPI based on interests
        for interest in interests:
            all_articles.extend(fetcher.fetch_news_api(interest, since=since))

        # 3. Deduplicate
        unique_articles = fetcher.deduplicate_articles(all_articles)
        print(f"Found {len(all_articles)} articles, reduced to {len(unique_articles)} after deduplication.")

        if not unique_articles:
            print(f"No new news for {email} today.")
            continue

        # 4. Summarize with Gemini
        summary = summarizer.summarize_articles(unique_articles, user_interests=interests)

        # 5. Distribute via Email
        date_str = datetime.now().strftime("%B %d, %Y")
        subject = f"Your Daily News Briefing - {date_str}"
        success = distributor.send_briefing(email, subject, summary)

        if success:
            print(f"Successfully sent briefing to {email}")
            # 6. Update state in Firestore
            db.update_last_sent(user_id)
        else:
            print(f"Failed to send briefing to {email}")

if __name__ == "__main__":
    main()

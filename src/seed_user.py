import os
from dotenv import load_dotenv
from infrastructure.db_factory import get_db_client

load_dotenv()

def seed():
    PROJECT_ID = os.getenv("PROJECT_ID")
    if not PROJECT_ID:
        print("Error: PROJECT_ID not found in .env")
        return

    db = get_db_client(project_id=PROJECT_ID)
    
    test_user_id = "test_user_001"
    test_email = os.getenv("SENDER_EMAIL") # Sending the brief to yourself for testing
    
    print(f"Adding test user to Firestore (Project: {PROJECT_ID})...")
    
    db.add_user(
        user_id=test_user_id,
        email=test_email,
        interests=["AI and Technology", "Global Economy", "Space Exploration"],
        rss_feeds=["https://feeds.bbci.co.uk/news/rss.xml"]
    )
    
    print(f"Successfully added user: {test_email}")

if __name__ == "__main__":
    seed()

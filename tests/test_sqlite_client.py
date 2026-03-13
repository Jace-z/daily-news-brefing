import pytest
import os
import sqlite3
import json
from src.infrastructure.sqlite_client import SQLiteClient

@pytest.fixture
def sqlite_client():
    db_path = "test_users.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Initialize schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            interests TEXT,
            rss_feeds TEXT,
            last_sent DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    
    client = SQLiteClient(db_path=db_path)
    yield client
    
    if os.path.exists(db_path):
        os.remove(db_path)

def test_add_and_get_user(sqlite_client):
    user_id = "test_1"
    email = "test@example.com"
    interests = ["tech", "ai"]
    rss_feeds = ["http://rss.com"]
    
    sqlite_client.add_user(user_id, email, interests, rss_feeds)
    
    profile = sqlite_client.get_user_profile(user_id)
    assert profile is not None
    assert profile['id'] == user_id
    assert profile['email'] == email
    assert profile['interests'] == interests
    assert profile['rss_feeds'] == rss_feeds

def test_get_user_profiles(sqlite_client):
    sqlite_client.add_user("u1", "u1@ex.com", ["a"], ["b"])
    sqlite_client.add_user("u2", "u2@ex.com", ["c"], ["d"])
    
    profiles = sqlite_client.get_user_profiles()
    assert len(profiles) == 2
    assert any(p['id'] == "u1" for p in profiles)
    assert any(p['id'] == "u2" for p in profiles)

def test_update_last_sent(sqlite_client):
    user_id = "test_update"
    sqlite_client.add_user(user_id, "test@ex.com", [], [])
    
    profile_before = sqlite_client.get_user_profile(user_id)
    assert profile_before['last_sent'] is None
    
    sqlite_client.update_last_sent(user_id)
    
    profile_after = sqlite_client.get_user_profile(user_id)
    assert profile_after['last_sent'] is not None

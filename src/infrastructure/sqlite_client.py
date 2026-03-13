import sqlite3
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional

class SQLiteClient:
    """
    Client for interacting with local SQLite to manage user profiles.
    """

    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_user_profiles(self) -> List[Dict]:
        """
        Retrieves all user profiles from SQLite.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        
        profiles = []
        for row in rows:
            profile = dict(row)
            profile['id'] = profile.pop('user_id')
            profile['interests'] = json.loads(profile['interests']) if profile['interests'] else []
            profile['rss_feeds'] = json.loads(profile['rss_feeds']) if profile['rss_feeds'] else []
            # Parse last_sent if it's a string
            if profile['last_sent'] and isinstance(profile['last_sent'], str):
                profile['last_sent'] = datetime.fromisoformat(profile['last_sent'])
            profiles.append(profile)
        
        conn.close()
        return profiles

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Retrieves a single user profile.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            profile = dict(row)
            profile['id'] = profile.pop('user_id')
            profile['interests'] = json.loads(profile['interests']) if profile['interests'] else []
            profile['rss_feeds'] = json.loads(profile['rss_feeds']) if profile['rss_feeds'] else []
            # Parse last_sent if it's a string
            if profile['last_sent'] and isinstance(profile['last_sent'], str):
                profile['last_sent'] = datetime.fromisoformat(profile['last_sent'])
            conn.close()
            return profile
        
        conn.close()
        return None

    def update_last_sent(self, user_id: str):
        """
        Updates the 'last_sent' timestamp for a user.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        now = datetime.now(timezone.utc).isoformat()
        cursor.execute("UPDATE users SET last_sent = ? WHERE user_id = ?", (now, user_id))
        conn.commit()
        conn.close()

    def add_user(self, user_id: str, email: str, interests: List[str], rss_feeds: List[str]):
        """
        Adds a new user profile.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        interests_json = json.dumps(interests)
        rss_feeds_json = json.dumps(rss_feeds)
        created_at = datetime.now(timezone.utc).isoformat()
        
        cursor.execute("""
            INSERT OR REPLACE INTO users (user_id, email, interests, rss_feeds, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, email, interests_json, rss_feeds_json, created_at))
        
        conn.commit()
        conn.close()

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    db_path = os.getenv("SQLITE_DB_PATH", "users.db")
    print(f"Initializing SQLite database at: {db_path}")
    
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
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()

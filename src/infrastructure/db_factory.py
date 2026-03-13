import os
from .firestore_client import FirestoreClient
from .sqlite_client import SQLiteClient

def get_db_client(project_id: str = None):
    provider = os.getenv("DB_PROVIDER", "firestore").lower()
    
    if provider == "sqlite":
        db_path = os.getenv("SQLITE_DB_PATH", "users.db")
        return SQLiteClient(db_path=db_path)
    elif provider == "firestore":
        if not project_id:
            project_id = os.getenv("PROJECT_ID")
            if not project_id:
                raise ValueError("PROJECT_ID environment variable is required for Firestore")
        return FirestoreClient(project_id=project_id)
    else:
        raise ValueError(f"Unsupported DB_PROVIDER: {provider}")

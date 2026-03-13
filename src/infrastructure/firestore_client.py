from google.cloud import firestore
from datetime import datetime, timezone
from typing import List, Dict, Optional

class FirestoreClient:
    """
    Client for interacting with Cloud Firestore to manage user profiles and state.
    """

    def __init__(self, project_id: str, collection_name: str = "users"):
        self.db = firestore.Client(project=project_id)
        self.collection_name = collection_name

    def get_user_profiles(self) -> List[Dict]:
        """
        Retrieves all user profiles from Firestore.
        """
        users_ref = self.db.collection(self.collection_name)
        docs = users_ref.stream()
        
        profiles = []
        for doc in docs:
            profile = doc.to_dict()
            profile['id'] = doc.id
            profiles.append(profile)
        return profiles

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Retrieves a single user profile.
        """
        user_ref = self.db.collection(self.collection_name).document(user_id)
        doc = user_ref.get()
        if doc.exists:
            profile = doc.to_dict()
            profile['id'] = doc.id
            return profile
        return None

    def update_last_sent(self, user_id: str):
        """
        Updates the 'last_sent' timestamp for a user.
        """
        user_ref = self.db.collection(self.collection_name).document(user_id)
        user_ref.update({
            'last_sent': datetime.now(timezone.utc)
        })

    def add_user(self, user_id: str, email: str, interests: List[str], rss_feeds: List[str]):
        """
        Adds a new user profile.
        """
        user_ref = self.db.collection(self.collection_name).document(user_id)
        user_ref.set({
            'email': email,
            'interests': interests,
            'rss_feeds': rss_feeds,
            'last_sent': None,
            'created_at': datetime.now(timezone.utc)
        })

if __name__ == "__main__":
    # Test (requires GCP authentication and active Firestore)
    # client = FirestoreClient(project_id="your-project-id")
    # client.add_user("test_user", "test@example.com", ["technology", "ai"], ["https://feeds.bbci.co.uk/news/rss.xml"])
    # print(client.get_user_profiles())
    pass

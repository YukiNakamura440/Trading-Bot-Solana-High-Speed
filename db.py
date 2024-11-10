from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    """MongoDB connection and data handling class."""
    
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client[os.getenv('DB_NAME')]
        self.collection = self.db['wallets']
    
    def get_user(self, user_id):
        """Fetch user data by user_id."""
        return self.collection.find_one({"user_id": user_id})

    def add_user(self, user_id, wallet_info):
        """Add user to the database."""
        self.collection.insert_one({"user_id": user_id, "wallet_info": wallet_info})
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import bcrypt
import re

load_dotenv()  # Load environment variables from .env file

# MongoDB setup using environment variable
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def register_user(telegram_user_id, email, password):
    if not validate_email(email):
        return False

    hashed_password = hash_password(password)
    user_data = {
        "telegram_user_id": telegram_user_id,
        "email": email,
        "password": hashed_password,
    }
    try:
        users_collection.insert_one(user_data)  # Try to insert the user data
        return True
    except Exception as e:
        print(f"Error inserting user data: {e}")  # Print any errors during insertion
        return False

def authenticate_user(email, password):
    user = users_collection.find_one({"email": email})
    if user and check_password(password, user['password']):
        return user
    return None

def check_user_exists(email):
    user = users_collection.find_one({"email": email})
    return user is not None
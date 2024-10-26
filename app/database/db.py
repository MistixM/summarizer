# Import all necessary dependencies for the database module
import firebase_admin

# Project uses Firebase as primary database
from firebase_admin import credentials
from firebase_admin import db

# Get credentials from the constants directory
cred = credentials.Certificate('./app/constants/firestore_key.json')

# Init database
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://summarizer-e7c00-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Create references
chat_ids_ref = db.reference('chat_ids')
users_ref = db.reference('users')

# Save chat ID to the database with default value (True)
def save_chat(chat_id: int) -> None:
    chat_ids_ref = db.reference('chat_ids')
    
    chat_data = {
        "vip": False
    }

    chat_ids_ref.child(str(chat_id)).set(chat_data)

# Check if a chat ID exists in the database
def check_chat(chat_id: int):
    chat_ids_ref = db.reference('chat_ids')
    return chat_ids_ref.child(str(chat_id)).get() is not None

# Check all the chat IDs
def get_all_chats() -> list:
    chat_ids = chat_ids_ref.get()

    return chat_ids.keys() if chat_ids else []

# Get all possible users from the database
def get_all_users() -> list:
    users = users_ref.get()
    return users.keys() if users else []

# Removes chat IDs from the database
def remove_chat(chat_id: int) -> None:
    chat_ids_ref = db.reference('chat_ids')
    chat_ids_ref.child(str(chat_id)).delete()

# Register a new user in the database
def register_user(chat_id: int, is_vip: bool, username: str):
    users_ref = db.reference('users')
    
    user_data = {
        "chat_id": chat_id,
        "is_vip": is_vip,
        "username": username if username else None
    }

    users_ref.child(str(chat_id)).set(user_data)

# Check if a user exists in the database
def check_user(chat_id: int):
    users_ref = db.reference('users')
    return users_ref.child(str(chat_id)).get() is not None

# Update user value in the database
def update_user_data(chat_id: int, data: str, value: str) -> None:
    ref = db.reference('users')
    ref.child(str(chat_id)).update({data: value})

# Update chat value in the database
def update_chat_data(chat_id: int, data: str, value: str) -> None:
    ref = db.reference('chat_ids')
    ref.child(str(chat_id)).update({data: value})

# Check requested user data
def check_user_data(user_id: int) -> None:
    ref = db.reference('users')
    return ref.child(str(user_id)).get()

# Check requested chat data
def check_chat_data(chat_id: int) -> None:
    ref = db.reference('chat_ids')
    return ref.child(str(chat_id)).get()
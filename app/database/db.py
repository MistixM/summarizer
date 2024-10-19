import firebase_admin

from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./app/constants/firestore_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://summarizer-e7c00-default-rtdb.europe-west1.firebasedatabase.app/'
})

chat_ids_ref = db.reference('chat_ids')
users_ref = db.reference('users')

# Save chat ID to the database with default value (True)
def save_chat(chat_id: int) -> None:
    chat_ids_ref = db.reference('chat_ids')
    chat_ids_ref.child(str(chat_id)).set(True)

# Check if a chat ID exists in the database
def check_chat(chat_id: int):
    chat_ids_ref = db.reference('chat_ids')
    return chat_ids_ref.child(str(chat_id)).get() is not None

# Check all the chat IDs
def get_all_chats() -> list:
    chat_ids = chat_ids_ref.get()

    return chat_ids.keys() if chat_ids else []

# Removes chat IDs from the database
def remove_chat(chat_id: int) -> None:
    chat_ids_ref = db.reference('chat_ids')
    chat_ids_ref.child(str(chat_id)).delete()

def register_user(chat_id: int, is_vip: bool):
    users_ref = db.reference('users')
    
    user_data = {
        "chat_id": chat_id,
        "is_vip": is_vip,
    }

    users_ref.child(str(chat_id)).set(user_data)

def check_user(chat_id: int):
    users_ref = db.reference('users')
    return users_ref.child(str(chat_id)).get() is not None
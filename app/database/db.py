import firebase_admin

from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./app/constants/firestore_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://summarizer-e7c00-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('chat_ids')

# Save chat ID to the database with default value (True)
def save_chat(chat_id: int) -> None:
    ref = db.reference('chat_ids')
    ref.child(str(chat_id)).set(True)

# Check if a chat ID exists in the database
def check_chat(chat_id: int):
    ref = db.reference('chat_ids')
    return ref.child(str(chat_id)).get() is not None

# Check all the chat IDs
def get_all_chats() -> list:
    chat_ids = ref.get()

    return chat_ids.keys() if chat_ids else []

def remove_chat(chat_id: int) -> None:
    ref = db.reference('chat_ids')
    ref.child(str(chat_id)).delete()
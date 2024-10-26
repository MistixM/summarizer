from cryptography.fernet import Fernet

from app.constants.wrap import (ENCRYPTION_KEY, VIP_FOLDER)
import os
import json

cipher = Fernet(ENCRYPTION_KEY)
os.makedirs(VIP_FOLDER, exist_ok=True)

async def save_encrypted_messages(chat_id, chat_messages) -> None:
    filename = os.path.join(VIP_FOLDER, f"{chat_id}.json")

    # Retreive chat messages and encrypt them
    data = json.dumps(chat_messages[chat_id])
    encrypted_data = cipher.encrypt(data.encode())

    with open(filename, 'wb') as file:
        file.write(encrypted_data)
    
    
async def decrypt_messages(chat_id) -> list:
    filename = os.path.join(VIP_FOLDER, f'{chat_id}.json')

    if not os.path.exists(filename):
        return None

    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    
    decrypted_data = cipher.decrypt(encrypted_data)
    messages = json.loads(decrypted_data.decode())

    return messages
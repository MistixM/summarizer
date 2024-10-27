# Import aiogram dependencies
from aiogram import Bot, types, Router
from aiogram.filters import Command

# Import other necessary dependencies from app
from app.utils.summarize_ai import summarize_messages
from app.utils.encryption import save_encrypted_messages, decrypt_messages

from app.constants.wrap import (BOT_COOLDOWN,  
                                NO_MESSAGE_SUMMARIZE,
                                ENCRYPTION_KEY)

from app.database.db import check_chat_data, check_chat

from cryptography.fernet import Fernet

from configparser import ConfigParser

# Other
import re
import asyncio
import os
import json

# Create a unique router for this handler
summarize_router = Router()

# Key for encryption
cipher = Fernet(ENCRYPTION_KEY)

# Directory for VIP chat files
# VIP_FOLDER = 'vip_chats'
# os.makedirs(VIP_FOLDER, exist_ok=True)

# Create dicts: messages and flags
chat_messages = {} # will be erased when the server is shut down
command_flags = {} # will be also erased when the server is shut down

# Init config parser
config = ConfigParser()
config.read('./app/constants/config.ini')

# Handler summarize command
@summarize_router.message(Command(commands=['sum']))
async def summarize_cmd(msg: types.Message, bot: Bot):
    # Define chat id and current chat data from database
    chat_id = msg.chat.id
    chat_data = check_chat_data(chat_id)

    # If it's not a group, notify about this
    if not '-' in str(chat_id):
        await bot.send_message(chat_id,
                               f"👀 <b>Please add me to the chat first</b>",
                               parse_mode='HTML',
                               disable_web_page_preview=True)
        return


    # Create filter for the command (to extract limit from the command)
    fltr = re.search(r'/sum (\d+)', msg.text)

    # Define limit from the command
    limit = int(fltr.group(1)) if fltr else 300

    # Handle other possible human mistakes
    # if limit < 0:
    #     await bot.send_message(chat_id, f"⚠️ Limit must be a positive number.")
    #     return
    # else:
    #     print(limit)
    #     print(type(limit))
        
    if not limit >= 10:
        await bot.send_message(chat_id, f"⚠️ Limit must be at least 10 messages.")
        return
    
    # If the chat is in cooldown, notify and return request
    if command_flags.get(chat_id, False):
        await bot.send_message(chat_id, BOT_COOLDOWN)
        return
    
    if not chat_data['vip']:
        # Get messages from the specified chat id
        messages = chat_messages.get(chat_id, [])
    else:
        messages = await decrypt_messages(chat_id)

    # If there are enough messages, summarize them and send to the chat id
    if messages:
        # Send request to OpenAI API via module with specified reverted limit
        summary = summarize_messages(messages[-limit:])

        # Send generated summarasing to the chat
        await bot.send_message(chat_id, summary)

        # Set delay for the chat
        command_flags[chat_id] = True

        # If chat is not vip, set default delay
        if not chat_data['vip']:
            await asyncio.sleep(int(config['Bot']['DELAY']))

        # Otherwise, set delay for vip chat
        else:
            await asyncio.sleep(int(config['Bot']['VIP_DELAY']))

        # Disable cooldown flag
        command_flags[chat_id] = False  

    # If there are no messages, notify the user about this
    else:
        await bot.send_message(chat_id, NO_MESSAGE_SUMMARIZE)

# Important. This router is blocking, so be careful with changes
# This handler will write each message that comes from the chat
@summarize_router.message()
async def handle_messages(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    if not check_chat(chat_id):
        return
    
    vip = check_chat_data(chat_id)['vip']

    # If it's a message, save it to temporary dictionary
    if msg.text:
        if chat_id not in chat_messages:
            chat_messages[chat_id] = []
        
        # Also include username if it's possible. Otherwise it will be "Anonymous"
        username = msg.from_user.username if msg.from_user.username else "Anonymous"

        # Convert messages to more friendly for the AI model
        chat_messages[chat_id].append(f"{username} said {msg.text[:100]}")

        if vip:
            await save_encrypted_messages(chat_id, chat_messages)

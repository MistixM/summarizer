from aiogram import Bot, types, Router
from aiogram.filters import Command

from app.utils.summarize_ai import summarize_messages
from app.constants.wrap import (BOT_COOLDOWN,  
                                NO_MESSAGE_SUMMARIZE)

from app.database.db import check_chat, save_chat

from configparser import ConfigParser

import re
import asyncio

summarize_router = Router()

chat_messages = {}
command_flags = {}

config = ConfigParser()
config.read('./app/constants/config.ini')

@summarize_router.message(Command(commands=['sum']))
async def summarize_cmd(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    if not '-' in str(chat_id):
        await bot.send_message(chat_id,
                               f"",
                               parse_mode='HTML',
                               disable_web_page_preview=True)
        return
    
    if command_flags.get(chat_id, False):
        await bot.send_message(chat_id, BOT_COOLDOWN)
        return
    
    fltr = re.search(r'/sum (\d+)', msg.text)
    limit = int(fltr.group(1)) if fltr else 300

    messages = chat_messages.get(chat_id, [])
    if messages:
        summary = summarize_messages(messages[-limit:])
        await bot.send_message(chat_id, summary)

        command_flags[chat_id] = True

        await asyncio.sleep(int(config['Bot']['DELAY']))

        command_flags[chat_id] = False

    else:
        await bot.send_message(chat_id, NO_MESSAGE_SUMMARIZE)

@summarize_router.message()
async def summarize_message(msg: types.Message):
    chat_id = msg.chat.id

    if "-" in str(chat_id) and not check_chat(chat_id):
        save_chat(chat_id)
    
    if msg.text:
        if chat_id not in chat_messages:
            chat_messages[chat_id] = []
        
        username = msg.from_user.username if msg.from_user.username else "Anonymous"

        chat_messages[chat_id].append(f"{username} said {msg.text[:100]}")

from aiogram import Bot, Router, types
from aiogram.filters import Command

from app.constants.wrap import ADMIN, FOUR_O_FOUR
from app.database.db import get_all_chats, remove_chat

ad_router = Router()

@ad_router.message(Command(commands=['ad']))
async def send_advertisement(msg: types.Message, bot: Bot):
    if not msg.chat.id == ADMIN:
        await bot.send_message(msg.chat.id,
                               FOUR_O_FOUR,
                               parse_mode='HTML')
        return
    
    chat_ids = get_all_chats()

    for chat in chat_ids:
        try:
            await bot.send_message(chat, '🍉 Watermelon')
        except Exception as e:
            # Remove chat from the database
            remove_chat(chat)
            print(f"An error occured while sending message: {e}")
            pass
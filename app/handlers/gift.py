from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError

from app.constants.wrap import ADMIN, FOUR_O_FOUR

from app.database.db import (update_user_data, get_all_chats, 
                             check_chat_data, update_chat_data, 
                             remove_chat)

import re
import datetime

gift_router = Router()

@gift_router.message(Command(commands=['gift']))
async def handle_gift(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    if not chat_id == ADMIN:
        await bot.send_message(msg.chat.id,
                                FOUR_O_FOUR,
                                parse_mode='HTML',
                                disable_web_page_preview=True)
        return

    fltr = re.search(r'/gift (\d+)(?:\s+(.+))?', msg.text)
    user_id = int(fltr.group(1)) if fltr else None
    custom_message = fltr.group(2) if fltr and fltr.group(2) else "Enjoy your VIP status!"

    if user_id:
        expiration_date = datetime.datetime.now() + datetime.timedelta(days=31)

        await bot.send_message(user_id,
                               f"🥳 <b>Congratulations! You just received a gift and now you are have a VIP status!</b>\n\nMessage from sender: <b>{custom_message}</b>\nExpiration date: <b>{expiration_date.strftime('%d.%m.%y')}</b>",
                               parse_mode='HTML')

        update_user_data(user_id, 'is_vip', True)
        update_user_data(user_id, "expiration_date", expiration_date.isoformat())
        update_user_data(user_id, "reminded", False)

        chats = get_all_chats()
        user = await bot.get_chat(user_id)

        for chat in chats:
            try:
                chat_info = check_chat_data(chat)
                owner = chat_info.get('b_owner')

                if owner and owner == chat_id:
                    update_chat_data(chat, "vip", True)
                    await bot.send_message(chat, f"🤩 Congratulations to @{user.username}! Now the chat has a VIP status", parse_mode='markdown')
                else:
                    continue
            except TelegramForbiddenError as e:
                if "bot was kicked" in str(e):
                    # Remove chat from database
                    print(f"The {chat} was removed from the database. Reason: Bot was kicked")
                    remove_chat(chat)
                    continue
                elif "the group chat was deleted" in str(e):
                    # Remove chat from database
                    print(f"The {chat} was removed from the database. Reason: The group chat was deleted")
                    remove_chat(chat)
                    continue
                else:
                    print(f"An unexpected error occured: {e}")
                    continue

    else:
        await bot.send_message(chat_id, "Something went wrong..")
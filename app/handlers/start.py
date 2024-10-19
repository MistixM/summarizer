from aiogram import Router, types, Bot
from aiogram.filters import Command

from app.constants.wrap import GROUP_START, DM_START
from app.keyboards.inline import add_bot
from app.database.db import register_user, check_user

start_router = Router()

@start_router.message(Command(commands=['help', 'start']))
async def start_message(msg: types.Message, bot: Bot):
    if "-" in str(msg.chat.id):
        await bot.send_message(msg.chat.id, 
                            GROUP_START,
                            disable_web_page_preview=True,
                            parse_mode='HTML')
    else:
        if not check_user(msg.chat.id):
            register_user(msg.chat.id, False)

        await bot.send_message(msg.chat.id,
                               DM_START,
                               disable_web_page_preview=True,
                               parse_mode='HTML',
                               reply_markup=add_bot())

@start_router.my_chat_member()
async def handle_bot_added(update: types.ChatMemberUpdated, bot: Bot):
    if update.new_chat_member.status == "member":
        added_by = update.from_user.id

        await bot.send_message(update.chat.id, f"Hurray! I was added by {added_by}")
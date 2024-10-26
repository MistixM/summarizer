# Import all necessary handlers, wraps and database modules and functions
from aiogram import Router, types, Bot
from aiogram.filters import Command

from app.constants.wrap import (GROUP_START, DM_START, VIP_FOLDER)
from app.keyboards.reply import menu_keyboard

from app.database.db import (register_user, 
                             check_user,
                             check_chat, 
                             save_chat,
                             update_chat_data, 
                             check_user_data,
                             remove_chat)

import os

# Create separate router
start_router = Router()

# Handle 'start' or 'help' commands
@start_router.message(Command(commands=['help', 'start']))
async def start_message(msg: types.Message, bot: Bot):
    try:
        # Something like filter. Will send group message only to the group
        if "-" in str(msg.chat.id):
            await bot.send_message(msg.chat.id, 
                                GROUP_START,
                                disable_web_page_preview=True,
                                parse_mode='HTML')
        
        # If it's not a group, just send DM message
        else:
            # Also check if user exist in database 
            # And if it's not, register them
            if not check_user(msg.chat.id):
                register_user(msg.chat.id, False, msg.from_user.username)

            await bot.send_message(msg.chat.id,
                                DM_START,
                                disable_web_page_preview=True,
                                parse_mode='HTML',
                                reply_markup=menu_keyboard(msg.chat.id))
    except Exception as e:
        print(f"[start.py] An error occured: {e}")

# Handler to check invite status
@start_router.my_chat_member()
async def handle_bot_added(update: types.ChatMemberUpdated, bot: Bot):

    # Check: who added the bot to the group
    if update.new_chat_member.status in ['member', 'administrator']:

        if not check_chat(update.chat.id):
            save_chat(update.chat.id)

        # Mandatory to save user that invited bot
        added_by = update.from_user.id
        
        # Again, if user does not exist in the database, just register
        if not check_user(added_by):
            register_user(added_by, False, update.from_user.username)

        # User info
        user = await update.bot.get_chat(added_by)
        
        # Database updates and checking 
        is_vip = check_user_data(added_by)['is_vip']
        update_chat_data(update.chat.id, "b_owner", added_by)

        # Vip status checking
        if is_vip:
            update_chat_data(update.chat.id, "vip", True)
            await bot.send_message(update.chat.id,
                                   f"🤩 Congratulations to @{user.username}! Now the chat has a VIP status",
                                   parse_mode='markdown')

    if update.new_chat_member.status in ['kicked', 'left']:
        os.remove(os.path.join(VIP_FOLDER, f'{update.chat.id}.json'))
        
        remove_chat(update.chat.id)

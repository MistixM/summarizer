# Advertisement module.

# Import all necessary modules to work with
from aiogram import Bot, Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# Import app and texts
from app.constants.wrap import ADMIN, FOUR_O_FOUR, POST_BUTTON
from app.database.db import get_all_chats

import re

# Create separate router
post_router = Router()

class PostState(StatesGroup):
    waiting_post = State()

# Limit set by default (None)
limit = None

# Create command handler
@post_router.message(Command(commands=['post']))
@post_router.message(lambda msg: msg.text == POST_BUTTON)
async def send_advertisement(msg: types.Message, bot: Bot, state: FSMContext):
    global limit

    # If it's not admin, send a message and deny access
    if not msg.chat.id == ADMIN:
        await bot.send_message(msg.chat.id,
                               FOUR_O_FOUR,
                               parse_mode='HTML',
                               disable_web_page_preview=True)
        return
    
    # Catch limit in the command and set None if it's not specified
    fltr = re.search(r'/post (\d+)', msg.text)
    limit = int(fltr.group(1)) if fltr else None
    
    await state.set_state(PostState.waiting_post)

    # Notify admin about further actions
    await bot.send_message(msg.chat.id, 
                           f"Please send the image and the caption for the post (limit: {limit})\n\n<b>FIY: If you want to cancel the process just use 'cancel' word</b>",
                           parse_mode='HTML')

@post_router.message(StateFilter(PostState.waiting_post), F.photo | F.text)
async def handle_post(msg: types.Message, bot: Bot, state: FSMContext):
    global limit

    await state.clear()

    if msg.photo:
        content_type = "photo"
        
        photo_id = msg.photo[-1].file_id
        caption = msg.caption if msg.caption else ''
    else:
        content_type = "text"
        content = msg.text

    if msg.text in ['cancel', 'Cancel']:
        await bot.send_message(msg.chat.id, "Action cancelled")
        return
    # Get all chat ids from the database
    chat_ids = list(get_all_chats())

    if limit:
        chat_ids = chat_ids[:limit]

    for chat in chat_ids:
        try:
            if content_type == "photo":
                await bot.send_photo(chat_id=chat,
                                    photo=photo_id,
                                    caption=caption,
                                    parse_mode='HTML'
                                    )
            else:
                await bot.send_message(chat_id=chat,
                                                text=content,
                                                parse_mode='HTML')
                
        except Exception as e:
            print(f"An error occured while sending message: {e}")
            pass
    
    await bot.send_message(msg.chat.id, f"Post with image and caption was sent")
    
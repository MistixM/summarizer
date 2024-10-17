from aiogram import Router, types, Bot
from aiogram.filters import Command

from app.constants.wrap import GROUP_START, DM_START
from app.keyboards.inline import add_bot

start_router = Router()

@start_router.message(Command(commands=['help', 'start']))
async def start_message(msg: types.Message, bot: Bot):
    if "-" in str(msg.chat.id):
        await bot.send_message(msg.chat.id, 
                            GROUP_START,
                            disable_web_page_preview=True,
                            parse_mode='HTML')
    else:
        
        await bot.send_message(msg.chat.id,
                               DM_START,
                               disable_web_page_preview=True,
                               parse_mode='HTML',
                               reply_markup=add_bot())
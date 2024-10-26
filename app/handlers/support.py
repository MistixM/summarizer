from aiogram import Bot, types, Router
from aiogram.filters import Command

from app.constants.wrap import SUPPORT_BUTTON, SUPPORT_MESSAGE

support_router = Router()

@support_router.message(Command(commands=['support']))
@support_router.message(lambda msg: msg.text == SUPPORT_BUTTON)
async def handle_support(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    await bot.send_message(chat_id,
                           SUPPORT_MESSAGE,
                           parse_mode='HTML',
                           disable_web_page_preview=True)
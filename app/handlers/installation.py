from aiogram import Bot, types, Router
from aiogram.filters import Command

from app.constants.wrap import INSTALLATION_BUTTON, INSTALLATION_MESSAGE
from app.keyboards.inline import add_bot

installation_router = Router()

@installation_router.message(Command(commands=['install']))
@installation_router.message(lambda msg: msg.text == INSTALLATION_BUTTON)
async def handle_installation(msg: types.Message, bot: Bot):
    await bot.send_message(msg.chat.id,
                           INSTALLATION_MESSAGE,
                           parse_mode='HTML',
                           reply_markup=add_bot())

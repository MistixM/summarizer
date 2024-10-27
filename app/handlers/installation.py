from aiogram import Bot, types, Router
from aiogram.filters import Command

from app.constants.wrap import INSTALLATION_BUTTON, INSTALLATION_MESSAGE
from app.keyboards.inline import add_bot

installation_router = Router()

@installation_router.message(Command(commands=['install']))
@installation_router.message(lambda msg: msg.text == INSTALLATION_BUTTON)
async def handle_installation(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id
    
    if not '-' in str(chat_id):
        await bot.send_message(chat_id,
                            INSTALLATION_MESSAGE,
                            parse_mode='HTML',
                            reply_markup=add_bot())
    else:
        await bot.send_message(chat_id,
                               f"<b>No need to reinstall me, I'm already installed</b> 😄\n\nIf you want to add me to another group, feel free to request in DM",
                               parse_mode='HTML')
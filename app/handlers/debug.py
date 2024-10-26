from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.constants.wrap import ADMIN, FOUR_O_FOUR, DEBUG_BUTTON

debug_router = Router()

@debug_router.message(Command(commands=['debug']))
@debug_router.message(lambda msg: msg.text == DEBUG_BUTTON)
async def handle_command(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    if not chat_id == ADMIN:
        await bot.send_message(chat_id,
                               FOUR_O_FOUR,
                               parse_mode='HTML')
        return

    debug_file = FSInputFile('bot.log')
    await bot.send_document(chat_id,
                            debug_file,
                            caption="✅ You're all set!")
from aiogram import Bot, Router, types
from aiogram.filters import Command

from app.constants.wrap import FAQS

faq_router = Router()

@faq_router.message(Command(commands=["faq"]))
async def faq_command(msg: types.Message, bot: Bot):
    faq = ""

    for title, answer in FAQS.items():
        faq += f"<b>{title}</b>\n{answer}\n\n"

    await bot.send_message(msg.chat.id, faq, parse_mode='HTML')

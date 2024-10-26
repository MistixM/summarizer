# FAQ module

# Import aiogram and app settings
from aiogram import Bot, Router, types
from aiogram.filters import Command

from app.constants.wrap import FAQS, FAQ_BUTTON

# Create separate router
faq_router = Router()

# Create command handler
@faq_router.message(Command(commands=["faq"]))
@faq_router.message(lambda msg: msg.text == FAQ_BUTTON)
async def faq_command(msg: types.Message, bot: Bot):
    # Create empty ref of FAQ (will be filled later)
    faq = ""

    # Check each title and answer in FAQ variable
    for title, answer in FAQS.items():
        faq += f"<b>{title}</b>\n{answer}\n\n"

    # Send FAQ to user
    await bot.send_message(msg.chat.id, faq, 
                           parse_mode='HTML',
                           disable_web_page_preview=True)

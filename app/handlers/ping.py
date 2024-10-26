# Import dependencies for bot and database
from aiogram import Bot, Router, types

# Create separate router
ping_router = Router()

# Handle ping command
@ping_router.message(lambda msg: msg.text and "ping" in msg.text.lower())
async def ping_check(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    if "-" in str(chat_id):
        await bot.send_message(msg.chat.id,
                            "pong")

from aiogram import Bot, Router, types

ping_router = Router()

@ping_router.message(lambda msg: msg.text and "ping" in msg.text.lower())
async def ping_check(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    if "-" in str(chat_id):
        await bot.send_message(msg.chat.id,
                            "pong")

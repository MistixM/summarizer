# Import bot dependencies
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.types import FSInputFile

# Import modules: handlers, databases, wraps..
from app.handlers import routers_list
from app.constants.wrap import LOCAL_TEST, ADMIN
from app.database.db import (check_user_data, 
                             get_all_users, 
                             update_user_data, 
                             check_chat_data, 
                             get_all_chats, 
                             update_chat_data)

# Import other libraries
import configparser
import asyncio
import datetime
import logging

# Initialize the dispatcher and include all possible routers
dp = Dispatcher()
dp.include_routers(*routers_list)

# logging.basicConfig(level=logging.DEBUG,
#                     format="{asctime} - {levelname} - {message}",
#                     style="{",
#                     filename='bot.log',
#                     encoding='utf-8',
#                     datefmt="%d.%m.%Y %H:%M")

async def main():
    # Create a session for Graspil API (statistics)
    session = AiohttpSession(
        api=TelegramAPIServer.from_base('https://67100b5e8a34b.tgrasp.co')
    )

    # Initialize and read bot configuration
    config = configparser.ConfigParser()
    config.read('app/constants/config.ini')

    # Create a bot conditions (either it's a local test or production)
    if not LOCAL_TEST:
        bot = Bot(token=config['Bot']['TOKEN'], session=session)
    else:
        bot = Bot(token=config['Bot']['TEST_TOKEN'])

    # Create task for vip status in a while loop
    asyncio.create_task(check_vip_status(bot))

    # Create polling for the bot
    await dp.start_polling(bot)

async def check_vip_status(bot: Bot):
    # Create loop for the bot
    while True:
        # Get all users from the database
        users = get_all_users()

        # Get all necessary time variables
        now = datetime.datetime.now()
        remind_days = datetime.timedelta(days=10)

        # Check each user and their vip status
        for user in users:
            user_data = check_user_data(user)

            user_chat = await bot.get_chat(user)
            
            vip_expire = user_data.get('expiration_date')

            if vip_expire:
                # Convert time from the database to bot's format
                converted_vip_expire = datetime.datetime.strptime(vip_expire, '%Y-%m-%dT%H:%M:%S.%f')

                # Calculate remaining time
                remaining_time = converted_vip_expire - now

                # And if remaining time equals 0 days, disable VIP status
                if remaining_time <= datetime.timedelta(0):    
                    # This needed to disable VIP for each group where bot exists
                    chats = get_all_chats()

                    # Update data for the user
                    update_user_data(user, "is_vip", False)
                    update_user_data(user, "expiration_date", None)
                    update_user_data(user, "reminded", None)

                    # Notify user in DM that subscription is over
                    await bot.send_message(user, f"📣 <b>Hello {user_chat.first_name}!</b>\n\nYour VIP status has expired. Use /subscription command to renew it!")
                    
                    # Check each chat and disable VIP status there in database
                    for chat in chats:
                        chat_info = check_chat_data(chat)
                        owner = chat_info.get("b_owner")

                        # Convert variables into the single variable type
                        if owner and str(owner) == str(user):

                            # Disable vip and send message to each chat
                            update_chat_data(chat, "vip", False)
                            await bot.send_message(chat, 
                                                   f"🟥 <b>VIP status has expired in this chat. @{user_chat.username} please renew it in bot's DM</b>",
                                                   parse_mode='markdown')

                # If it's not final day, just send a reminder to the user's DM
                elif remaining_time <= remind_days and not user_data.get('reminded'):
                    update_user_data(user, "reminded", True)
                    await bot.send_message(user, f"⚠️ Hello {user_chat.first_name}. Your VIP status will expire in {remaining_time.days} days. You can renew it after expiration again! 😊")
        

        # 24 hours
        await asyncio.sleep(86400)

        debug_file = FSInputFile('bot.log')
        await bot.send_document(ADMIN, debug_file, caption="✅ <b>Hello! Here's your daily log. Don't forget to clear and review it from time to time</b>", parse_mode='HTML')

if __name__ == '__main__':
    # Run bot
    try:
        logging.info("Bot started")
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit, SystemError):
        logging.info("Bot stopped")
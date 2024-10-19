from aiogram import Bot, Dispatcher
from app.handlers import routers_list
from app.constants.wrap import LOCAL_TEST

import configparser
import asyncio

async def main():
    config = configparser.ConfigParser()
    config.read('app/constants/config.ini')

    if not LOCAL_TEST:
        bot = Bot(token=config['Bot']['TOKEN'])
    else:
        bot = Bot(token=config['Bot']['TEST_TOKEN'])

    dp = Dispatcher()

    dp.include_routers(*routers_list)
    
    await dp.start_polling(bot)

if __name__ == '__main__':

    try:
        print("Bot started")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, SystemError):
        print("Bot stopped")
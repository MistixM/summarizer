from aiogram import Bot, Dispatcher
from app.handlers import routers_list

import configparser
import asyncio

async def main():

    config = configparser.ConfigParser()
    config.read('app/constants/config.ini')

    bot = Bot(token=config['Bot']['TOKEN'])

    dp = Dispatcher()

    dp.include_routers(*routers_list)
    
    await dp.start_polling(bot)

if __name__ == '__main__':

    try:
        print("Bot started")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, SystemError):
        print("Bot stopped")
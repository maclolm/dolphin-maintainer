import asyncio
import logging
import config
from aiogram import Bot, Dispatcher

from handlers import owner_handler, start_handler, sub_handler
from dbcontroller import DBcontroller

logging.basicConfig(level=logging.INFO)
db = DBcontroller(config.dbfile)

class SubStatus:
    ACTUAL = 1
    UNKNOWN = 0
    EXPIRED = -1

async def main():
    db.init()

    bot = Bot(token=config.token)
    dispatcher = Dispatcher()
    dispatcher.include_routers(owner_handler.router, start_handler.router, sub_handler.router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

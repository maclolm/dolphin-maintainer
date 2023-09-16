import asyncio
import logging
import config
from aiogram import Bot, Dispatcher

from handlers import owner_handler, start_handler, sub_handler
from dbcontroller import DataBaseController
from scheduler.scheduler import Scheduler

logging.basicConfig(level=logging.INFO)
db = DataBaseController(config.dbfile)
dispatcher = Dispatcher()
bot = Bot(token=config.token)


class SubStatus:
    ACTUAL = 2
    EXPIRED = -2
    EXPIRED_SOON = -1


async def main():
    try:
        db.init()

        scheduler = Scheduler()
        scheduler.start_polling()

        dispatcher.include_routers(owner_handler.router, start_handler.router, sub_handler.router)
        await dispatcher.start_polling(bot)

    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

import asyncio
import logging
import config
from aiogram import Bot, Dispatcher

from routers import sub_router
from dbcontroller import DBcontroller

logging.basicConfig(level=logging.INFO)
db = DBcontroller(config.dbfile)


async def main():
    bot = Bot(token=config.token)
    dispatcher = Dispatcher()
    dispatcher.include_routers(sub_router.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

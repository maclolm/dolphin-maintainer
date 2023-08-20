import asyncio
import logging
import config
from aiogram import Bot, Dispatcher

from dbcontroller import DBcontroller
import router

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.token)
    dispatcher = Dispatcher()
    dispatcher.include_routers(router.main_router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

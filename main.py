import asyncio
import logging
from config import SessionData
import yaml

from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage
from bot.middlewares import StartMessageMiddleware, OwnerMessageMiddleware, SubscriberMessageMiddleware
from bot.handlers import owner_handler, start_handler, sub_handler
from dbcontroller.dbcontroller import DataBaseController
from scheduler.scheduler import Scheduler

DEFAULT_CONFIG = "config.yaml"

db = DataBaseController()

logging.basicConfig(level=logging.INFO)


def parse_config(file):
    with open(file, 'r') as config_file:
        data = yaml.safe_load(config_file)

    tg_token = data["token"]
    config = SessionData(
        session_username=data["session_username"],
        api_hash=data["api_hash"],
        api_id=data["api_id"]
    )
    payments_provider_token = data['payments_provider_token']

    return config, tg_token, payments_provider_token


async def main():
    try:
        session_data, token, payments_provider_token = parse_config(DEFAULT_CONFIG)

        db.init()

        bot = Bot(token=token)

        start_middleware = StartMessageMiddleware(session_data)
        start_handler.router.message.middleware(start_middleware)

        owner_middleware = OwnerMessageMiddleware(session_data)
        owner_handler.router.message.middleware(owner_middleware)

        sub_middleware = SubscriberMessageMiddleware(payments_provider_token)
        sub_handler.router.message.middleware(sub_middleware)

        storage = MemoryStorage()
        dispatcher = Dispatcher(storage=storage)
        dispatcher.include_routers(owner_handler.router, start_handler.router, sub_handler.router)

        scheduler = Scheduler(bot, session_data)
        scheduler.start_polling()

        await dispatcher.start_polling(bot)
        await bot.session.close()

    except Exception as ex:
        logging.exception(ex)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

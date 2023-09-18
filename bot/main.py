import asyncio
import logging
from config import Config
import yaml

from aiogram import Bot, Dispatcher

from handlers import owner_handler, start_handler, sub_handler
from dbcontroller import DataBaseController
from scheduler import Scheduler

DEFAULT_CONFIG = "config.yaml"
DB_FILE = 'dolphin-subscribers.db'

db = DataBaseController(DB_FILE)

logging.basicConfig(level=logging.INFO)


def parse_config(file):
    with open(file, 'r') as config_file:
        data = yaml.safe_load(config_file)

    config = Config(
        session_username=data["session_username"],
        token=data["token"],
        api_hash=data["api_hash"],
        api_id=data["api_id"],
        db_file=data["dbfile"]
    )

    return config


async def main():
    try:
        config = parse_config(DEFAULT_CONFIG)

        db.init()

        dispatcher = Dispatcher()
        bot = Bot(token=config.token)

        scheduler = Scheduler(config.db_file, bot)
        scheduler.start_polling()

        dispatcher.include_routers(owner_handler.router, start_handler.router, sub_handler.router)

        await dispatcher.start_polling(bot)
        await bot.session.close()

    except Exception as ex:
        logging.error(ex)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

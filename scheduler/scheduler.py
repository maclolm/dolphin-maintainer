from datetime import datetime
from logging import getLogger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dbcontroller import DataBaseController
from config import dbfile
from bot.handlers.sub_handler import send_subscription_remind_message

log = getLogger('scheduler')
RECALC_TUSK_TIME = 4
REMINDING_TASK_TIME = 5


class Scheduler(AsyncIOScheduler):

    @staticmethod
    def __decrease_sub_days():
        log.info('Sub days decreasing started by scheduler')

        with DataBaseController(dbfile) as db_conn:
            db_conn.decrease_subscription_days()

    @staticmethod
    def __recalc_sub_status():
        log.info('Sub status recalculation started by scheduler')

        with DataBaseController(dbfile) as db_conn:
            db_conn.recalc_sub_status()

    @staticmethod
    async def __schedule_reminding_task():
        with DataBaseController(dbfile) as db_conn:
            await send_subscription_remind_message(db_conn)

    def __schedule_recalc_tasks(self):
        self.__decrease_sub_days()
        self.__recalc_sub_status()

    def start_polling(self):
        self.add_job(self.__schedule_recalc_tasks, "cron", hour=RECALC_TUSK_TIME)
        self.add_job(self.__schedule_reminding_task, "cron", hour=REMINDING_TASK_TIME)
        self.start()

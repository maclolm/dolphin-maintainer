from logging import getLogger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dbcontroller import DataBaseController

log = getLogger('scheduler')
RECALC_TUSK_TIME = 4
REMINDING_TASK_TIME = 5


class Scheduler(AsyncIOScheduler):
    def __init__(self, db_file, bot):
        super().__init__()
        self.db_file = db_file
        self.tg_bot = bot

    async def __send_subscription_remind_message(self):
        with DataBaseController(self.db_file) as db_conn:
            expired_subs = db_conn.get_expired_subs()

            # TODO: Inline-кнопка для оплаты
            for tg_id, days_to_expire in expired_subs:
                if days_to_expire == 0:
                    await self.tg_bot.send_message(text=f"Твоя подписка закончилась.", chat_id=tg_id)
                    continue
                await self.tg_bot.send_message(
                    text=f"Твоя подписка заканчивается через {days_to_expire} дней. Не забудь продлить.",
                    chat_id=tg_id
                )

    def __decrease_sub_days(self):
        log.info('Sub days decreasing started by scheduler')

        with DataBaseController(self.db_file) as db_conn:
            db_conn.decrease_subscription_days()

    def __recalc_sub_status(self):
        log.info('Sub status recalculation started by scheduler')

        with DataBaseController(self.db_file) as db_conn:
            db_conn.recalc_sub_status()

    async def __schedule_reminding_task(self):
        log.info('Reminding subs about subscription started by scheduler')
        await self.__send_subscription_remind_message()

    def __schedule_recalc_tasks(self):
        self.__decrease_sub_days()
        self.__recalc_sub_status()

    def start_polling(self):
        self.add_job(self.__schedule_recalc_tasks, "cron", hour=RECALC_TUSK_TIME)
        self.add_job(self.__schedule_reminding_task, "cron", hour=REMINDING_TASK_TIME)
        self.start()

from logging import getLogger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import SessionData
from bot.handlers.routers_helper import refresh_all_users

log = getLogger('scheduler')
RECALC_TUSK_TIME = 4
UPDATE_SUBS_INFO_TIME = 5
REMINDING_TASK_TIME = 5


class Scheduler(AsyncIOScheduler):
    def __init__(self, bot, session_data):
        super().__init__()
        self.tg_bot = bot
        self.session_data: SessionData = session_data

    def start_polling(self):
        self.add_job(self.__schedule_update_subs_info, "cron", hour=UPDATE_SUBS_INFO_TIME)
        self.add_job(self.__schedule_recalc_tasks, "cron", hour=RECALC_TUSK_TIME)
        self.add_job(self.__schedule_reminding_task, "cron", hour=REMINDING_TASK_TIME)
        self.start()

    async def __schedule_reminding_task(self):
        log.info('Reminding subs about subscription is started by scheduler')
        await self.__send_subscription_remind_message()

    async def __schedule_update_subs_info(self):
        log.info('Updating of ids of all users is started by the scheduler')
        await refresh_all_users(self.session_data)

    def __schedule_recalc_tasks(self):
        self.__decrease_sub_days()
        self.__recalc_sub_status()

    async def __send_subscription_remind_message(self):
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

    @staticmethod
    def __decrease_sub_days():
        log.info('Sub days decreasing is started by scheduler')
        db_conn.decrease_subscription_days()

    @staticmethod
    def __recalc_sub_status():
        log.info('Sub status recalculation is started by scheduler')
        db_conn.recalc_sub_status()

from aiogram import Router, F
from aiogram.types import Message

from bot.messages import BotButtons
from bot.middlewares import SubscriberMessageMiddleware

import main

router = Router()
router.message.middleware(SubscriberMessageMiddleware())


# TODO: сделать inline-кнопку с функционалом renew_subscription к сообщению, если срок подписки закончился
@router.message(F.text == BotButtons.DAYS_TO_EXPIRE)
async def days_to_expire(message: Message):
    tg_user_id = message.from_user.id
    days = main.db.get_sub_days(tg_user_id)
    if days > 0:
        await message.reply(f"{message.from_user.first_name}, оплата твоей подписки истекает через {days} дней")
    elif days == -1:
        await message.reply(f"Похоже, твоя подписка бесконечна (по крайней мере пока что...)")
    else:
        await message.reply(f"{message.from_user.first_name}, Твоя подписка не оплачена 🥺")


@router.message(F.text == BotButtons.RENEW_SUBSCRIPTION)
async def renew_subscription(message: Message):
    await message.reply(f"Продление подписки ещё не добавили :(")

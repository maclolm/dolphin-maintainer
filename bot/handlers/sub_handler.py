import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from bot import permissions
from bot.messages import BotMessages, BotButtons
from bot import bot_main

router = Router()


# TODO: сделать inline-кнопку с функционалом renew_subscription к сообщению, если срок подписки закончился
@router.message(F.text == BotButtons.DAYS_TO_EXPIRE)
@permissions.is_sub
async def days_to_expire(message: Message):
    tg_user_id = message.from_user.id
    days = bot_main.db.get_sub_days(tg_user_id)
    if days > 0:
        await message.reply(f"{message.from_user.first_name}, оплата твоей подписки истекает через {days} дней")
    elif days == -1:
        await message.reply(f"Похоже, твоя подписка бесконечна (по крайней мере пока что...)")
    else:
        await message.reply(f"{message.from_user.first_name}, Твоя подписка не оплачена 🥺")


@router.message(F.text == BotButtons.RENEW_SUBSCRIPTION)
@permissions.is_sub
async def renew_subscription(message: Message):
    await message.reply(f"Оплату подписки ещё не добавили :(")

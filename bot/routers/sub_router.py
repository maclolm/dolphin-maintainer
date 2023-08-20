from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from bot.bot import db

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [KeyboardButton(text="Дней до окончания подписки")],
        [KeyboardButton(text="Продлить подписку")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                         resize_keyboard=True,
                                         input_field_placeholder='Выберите действие.'
                                         )
    await message.answer("Привет👋. Я тестовый бот управления подпиской", reply_markup=keyboard)


@router.message(F.text.lower() == "дней до окончания подписки")
async def days_to_expire(message: Message):
    subname = ''
    days = db.get_sub_days(subname)
    if days > 0:
        await message.reply(f"ID: {message.from_user.id} Оплата твоей подписки истекает через {days} дней")
    else:
        await message.reply(f"ID: {message.from_user.id} Твоя подписка не оплачена 🥺")


@router.message(F.text.lower() == "продлить подписку")
async def renew_subscription(message: Message):
    pass

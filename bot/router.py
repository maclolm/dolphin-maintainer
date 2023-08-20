import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

import config
from dbcontroller import DBcontroller
from messages import BotMessages, BotButtons

main_router = Router()
db = DBcontroller(config.dbfile)
db.init()

@main_router.message(Command("start"))
async def cmd_start(message: Message):
    logging.info(f'User {message.from_user.username}:{message.from_user.id} start chat')

    unsub_buttons = [
        [KeyboardButton(text=BotButtons.INFO)],
        [KeyboardButton(text=BotButtons.TARIFF)]
    ]
    kb = unsub_buttons

    subs = db.get_sub_ids()
    if (message.from_user.id,) in subs:
        sub_buttons = [
            [KeyboardButton(text=BotButtons.DAYS_TO_EXPIRE)],
            [KeyboardButton(text=BotButtons.RENEW_SUBSCRIPTION)]
        ]
        kb.extend(sub_buttons)

    owners = db.get_owner_ids()
    if (message.from_user.id,) in owners:
        kb = [
            [KeyboardButton(text=BotButtons.STATS_FOR_OWNER)],
            [KeyboardButton(text=BotButtons.GET_SUB_INFO)],
            [KeyboardButton(text=BotButtons.ADD_SUB)],
            [KeyboardButton(text=BotButtons.DEL_SUB)]
        ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Выберите действие.'
                                   )
    await message.answer("Привет👋. Я тестовый бот управления подпиской", reply_markup=keyboard)


# --- Ubsub and Sub messages ---
@main_router.message(F.text == BotButtons.INFO)
async def get_info(message: Message):
    await message.reply(f"Текст с общей информацией о VIP-канале.")


@main_router.message(F.text == BotButtons.TARIFF)
async def get_tariff(message: Message):
    await message.reply(f"Текст с ценами и тарифами к оплате")


# TODO: сделать inline-кнопку с функционалом renew_subscription к сообщению, если срок подписки закончился
# --- Subscriber messages ---
@main_router.message(F.text == BotButtons.DAYS_TO_EXPIRE)
async def days_to_expire(message: Message):
    subname = ''
    days = db.get_sub_days(subname)
    if days > 0:
        await message.reply(f"ID: {message.from_user.id} Оплата твоей подписки истекает через {days} дней")
    else:
        await message.reply(f"ID: {message.from_user.id} Твоя подписка не оплачена 🥺")


@main_router.message(F.text == BotButtons.RENEW_SUBSCRIPTION)
async def renew_subscription(message: Message):
    await message.reply(f"Оплату подписки ещё не добавили :(")


# --- Owner messages ---
@main_router.message(F.text == BotButtons.STATS_FOR_OWNER)
async def get_owner_stats(message: Message):
    await message.reply(f"Статистики для администратора пока нет")


@main_router.message(F.text == BotButtons.GET_SUB_INFO)
async def get_sub_info(message: Message):
    await message.reply(f"Пока невозможно узнать информацию о конкретном подписчике")


@main_router.message(F.text == BotButtons.ADD_SUB)
async def add_sub(message: Message):
    await message.reply(f"Пока невозможно добавить подписчика в систему")


@main_router.message(F.text == BotButtons.DEL_SUB)
async def delete_sub(message: Message):
    await message.reply(f"Пока невозможно удалить подписчика из системы")

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from bot.bot import db

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    unsub_buttons = [
        [KeyboardButton(text="Информация")],
        [KeyboardButton(text="Цены и тарифы")]
    ]
    kb = unsub_buttons

    subs = db.get_subs()
    if message.from_user.id in subs:
        sub_buttons = [
            [KeyboardButton(text="Дней до окончания подписки")],
            [KeyboardButton(text="Продлить подписку")]
        ]
        kb.extend(sub_buttons)

    owners = db.get_owners()
    if message.from_user.id in owners:
        kb = [
            [KeyboardButton(text="Статистика")],
            [KeyboardButton(text="Информация о подписчике")],
            [KeyboardButton(text="Добавить подписчика")],
            [KeyboardButton(text="Удалить подписчика")]
        ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Выберите действие.'
                                   )
    await message.answer("Привет👋. Я тестовый бот управления подпиской", reply_markup=keyboard)


# --- Ubsub and Sub messages ---
@router.message(F.text.lower() == "информация")
async def days_to_expire(message: Message):
    await message.reply(f"Текст с общей информацией о VIP-канале.")


@router.message(F.text.lower() == "цены и тарифы")
async def days_to_expire(message: Message):
    await message.reply(f"Текст с ценами и тарифами к оплате")


# TODO: сделать inline-кнопку с функционалом renew_subscription к сообщению, если срок подписки закончился
# --- Subscriber messages ---
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


# --- Owner messages ---
@router.message(F.text.lower() == "Статистика")
async def days_to_expire(message: Message):
    await message.reply(f"Статистики для администратора пока нет")


@router.message(F.text.lower() == "Информация о подписчике")
async def days_to_expire(message: Message):
    await message.reply(f"Пока невозможно узнать информацию о конкретном подписчике")


@router.message(F.text.lower() == "Добавить подписчика")
async def days_to_expire(message: Message):
    await message.reply(f"Пока невозможно добавить подписчика в систему")


@router.message(F.text.lower() == "Удалить подписчика")
async def days_to_expire(message: Message):
    await message.reply(f"Пока невозможно удалить подписчика из системы")

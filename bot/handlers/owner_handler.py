import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.messages import BotMessages, BotButtons
from .routers_helper import get_user_id
from bot import permissions, bot_main

router = Router()


# -- Start add subscriber section
class AddSubscriberForm(StatesGroup):
    waiting_for_username = State()
    waiting_for_start_sub_days = State()


@router.message(F.text == BotButtons.ADD_SUB)
@permissions.is_owner
async def sub_add(message: Message, state: FSMContext):
    await message.reply(f"Введите *username* пользователя в телеграм для добавления (без @)")
    await state.set_state(AddSubscriberForm.waiting_for_username)


@router.message(AddSubscriberForm.waiting_for_username)
async def sub_username_chosen(message: Message, state: FSMContext):
    username = message.text
    try:
        user_id = await get_user_id(username)
    except ValueError as ex:
        await message.answer(text=f"Похоже, пользователя с username '{username}' не существует.")
        await state.clear()
        return

    await state.update_data(username=message.text)
    await state.update_data(tg_id=user_id)

    await message.answer(text="Отлично. Задайте начальное количество дней подписки (-1: бессрочно)")
    await state.set_state(AddSubscriberForm.waiting_for_start_sub_days)


@router.message(AddSubscriberForm.waiting_for_start_sub_days)
async def sub_start_subscription_days_chosen(message: Message, state: FSMContext):
    await state.update_data(start_sub_days=message.text)
    user_data = await state.get_data()
    username = user_data['username']
    start_sub_days = user_data['start_sub_days']
    user_id = user_data['tg_id']

    await message.reply(f"Добавление {username} в таблицу подписчиков...")
    bot_main.db.add_to_sub_table(user_id, username, start_sub_days)

    await message.reply(f"Name {username} id: {user_id} успешно добавлен таблицу.")

# -- End add subscriber section


@router.message(F.text == BotButtons.STATS_FOR_OWNER)
@permissions.is_owner
async def get_owner_stats(message: Message):
    await message.reply(f"Статистики для администратора пока нет")


@router.message(F.text == BotButtons.GET_SUB_INFO)
@permissions.is_owner
async def get_sub_info(message: Message):
    await message.reply(f"Пока невозможно узнать информацию о конкретном подписчике")


@router.message(F.text == BotButtons.DEL_SUB)
@permissions.is_owner
async def delete_sub(message: Message):
    await message.reply(f"Пока невозможно удалить подписчика из системы")


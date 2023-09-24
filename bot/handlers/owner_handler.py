from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from dbcontroller import ExistsError
from bot.middlewares import OwnerMessageMiddleware
from bot.messages import BotButtons
from bot.handlers.routers_helper import get_user_id
from bot import permissions

import main

router = Router()


# -- Start add subscriber section
class AddSubscriberForm(StatesGroup):
    waiting_for_username = State()
    waiting_for_start_sub_days = State()


@router.message(F.text == BotButtons.ADD_SUB)
async def sub_add(message: Message, state: FSMContext):
    await message.reply(f"Введите username пользователя в телеграм для добавления в подписчики.")
    await state.set_state(AddSubscriberForm.waiting_for_username)


@router.message(AddSubscriberForm.waiting_for_username)
async def sub_username_chosen(message: Message, state: FSMContext):
    username = message.text
    user_data = await state.get_data()
    try:
        user_id = await get_user_id(username, user_data['session_data'])
    except ValueError as ex:
        await message.answer(text=f"Похоже, пользователя с username '{username}' не существует.")
        await state.clear()
        return

    await state.update_data(username=username)
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

    await message.answer(f"Добавление {username} ...")
    main.db.add_to_sub_table(user_id, username, start_sub_days)

    await message.answer(f"Пользователь {username} id: {user_id} успешно добавлен таблицу подписчиков.")
    await state.clear()
# -- End add subscriber section


# -- Start add owner section
class AddOwnerForm(StatesGroup):
    waiting_for_username = State()


@router.message(F.text == BotButtons.ADD_OWNER)
async def owner_add(message: Message, state: FSMContext):
    await message.answer(f"Введите username пользователя в телеграм для добавления в владельцы")
    await state.set_state(AddOwnerForm.waiting_for_username)


@router.message(AddOwnerForm.waiting_for_username)
async def owner_username_chosen(message: Message, state: FSMContext):
    username = message.text
    user_data = await state.get_data()
    try:
        user_id = await get_user_id(username, user_data['session_data'])
    except ValueError as ex:
        await message.answer(text=f"Похоже, пользователя с username '{username}' не существует.")
        await state.clear()
        return

    await message.answer(f"Добавление {username}...")
    main.db.add_to_owner_table(user_id, username)

    await message.answer(f"Пользователь {username} id: {user_id} успешно добавлен таблицу владельцев.")
    await state.clear()
# -- End add owner section


@router.message(F.text == BotButtons.STATS_FOR_OWNER)
async def get_global_stats(message: Message):
    subs = main.db.get_all_subs()
    subs_string = 'ID|  [NICKNAME]  -  [STATUS | DAYS]\n'
    for sub_id, _, username, creation_datetime, status, sub_days in subs:
        sub_str = '{:<d} | [{:<s}]  -  [{:<s} | {:<d}]\n'.format(sub_id, username, status, sub_days)
        subs_string += sub_str

    await message.answer(subs_string)


# -- Start sub info section
class GetSubStatsForm(StatesGroup):
    waiting_for_username = State()


@router.message(F.text == BotButtons.GET_SUB_INFO)
async def get_sub_info(message: Message, state: FSMContext):
    await message.reply(f"Введите *username* пользователя в телеграм для получения статистики")
    await state.set_state(GetSubStatsForm.waiting_for_username)


@router.message(GetSubStatsForm.waiting_for_username)
async def sub_username_chosen(message: Message, state: FSMContext):
    username = message.text
    user_data = await state.get_data()
    try:
        user_id = await get_user_id(username, user_data['session_data'])
        days, status = main.db.get_sub_stats(user_id)
    except ExistsError:
        await message.reply(f"Пользователя {username} не существует в таблице (или он сменил username)")
        await state.clear()
        return

    await message.reply(f"{username} | Статус: {status} | Дней: {days}")
    await state.clear()
# -- End sub stats section


# -- Start sub delete section
class DeleteSubscriberForm(StatesGroup):
    waiting_for_username = State()


@router.message(F.text == BotButtons.DEL_SUB)
async def delete_sub(message: Message, state: FSMContext):
    await message.reply(f"Введите username пользователя в телеграм для удаления из таблицы подписчиков")
    await state.set_state(DeleteSubscriberForm.waiting_for_username)


@router.message(DeleteSubscriberForm.waiting_for_username)
async def sub_username_chosen(message: Message, state: FSMContext):
    username = message.text
    user_data = await state.get_data()
    await message.answer(f"Удаление {username}...")
    try:
        user_id = await get_user_id(username, user_data['session_data'])
        main.db.delete_from_sub_table(user_id)
    except ExistsError:
        await message.reply(f"Пользователя {username} не существует в таблице (или он сменил username)")
        await state.clear()
        return

    await message.answer(f"Пользователь {username} id: {user_id} успешно удалён из таблицы подписчиков.")
    await state.clear()
# -- End sub delete section


# -- Start owner delete section
class DeleteOwnerForm(StatesGroup):
    waiting_for_username = State()


@router.message(F.text == BotButtons.DEL_OWNER)
async def delete_owner(message: Message, state: FSMContext):
    await message.reply(f"Введите username пользователя в телеграм для удаления из таблицы владельцев")
    await state.set_state(DeleteOwnerForm.waiting_for_username)


@router.message(DeleteOwnerForm.waiting_for_username)
async def owner_username_chosen(message: Message, state: FSMContext):
    username = message.text
    user_data = await state.get_data()
    await message.answer(f"Удаление {username} ...")
    try:
        user_id = await get_user_id(username, user_data['session_data'])
        main.db.delete_from_owner_table(user_id)
    except ExistsError:
        await message.reply(f"Пользователя {username} не существует в таблице (или он сменил username)")
        await state.clear()
        return

    await message.answer(f"Пользователь {username} id: {user_id} успешно удалён из таблицы владельцев")
    await state.clear()
# -- End owner delete section

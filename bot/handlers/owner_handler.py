import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from bot.messages import BotMessages, BotButtons
from.routers_helper import get_user_id
from bot import permissions

router = Router()


@router.message(F.text == BotButtons.STATS_FOR_OWNER)
@permissions.is_owner
async def get_owner_stats(message: Message):
    await message.reply(f"Статистики для администратора пока нет")


@router.message(F.text == BotButtons.GET_SUB_INFO)
@permissions.is_owner
async def get_sub_info(message: Message):
    await message.reply(f"Пока невозможно узнать информацию о конкретном подписчике")


@router.message(F.text == BotButtons.ADD_SUB)
@permissions.is_owner
async def add_sub(message: Message):
    await message.reply(f"Пока невозможно добавить подписчика")
    # user_tg_id = await get_user_id(message.from_user.username)
    # await message.reply(f"Name {message.from_user.username} id: {user_tg_id}")


@router.message(F.text == BotButtons.DEL_SUB)
@permissions.is_owner
async def delete_sub(message: Message):
    await message.reply(f"Пока невозможно удалить подписчика из системы")


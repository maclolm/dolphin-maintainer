from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()  # [1]

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    await message.answer("Привет. Я бот оплаты подписки.")

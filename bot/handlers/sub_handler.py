from aiogram import Router, F, types, Bot
from aiogram.types import Message
from aiogram.types.message import ContentType


from bot.messages import BotButtons, BotMessages
from aiogram.fsm.context import FSMContext

import main

router = Router()


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


# Setup prices
PRICES = [
    types.LabeledPrice(label='Подписка на месяц', amount=500),
    types.LabeledPrice(label='Подписка на 3 месяца', amount=1200),
    types.LabeledPrice(label='Подписка на год', amount=4000)
]


@router.message(F.text == BotButtons.RENEW_SUBSCRIPTION)
async def renew_subscription(message: Message, state: FSMContext):
    await message.answer("Оплата недоступна.")


#     sub_data = await state.get_data()
#     payments_token = sub_data['payments_provider_token']
#     if payments_token.split(':')[1] == 'TEST':
#         await message.answer("Сейчас оплата работает в тестовом режиме")
#
#     bot = Bot.get_current()
#     await bot.send_invoice(
#         message.chat.id,
#         title="Test title",
#         description="Test description",
#         provider_token=payments_token,
#         currency='rub',
#         # photo_url=TIME_MACHINE_IMAGE_URL,
#         # photo_height=512,  # !=0/None or picture won't be shown
#         # photo_width=512,
#         # photo_size=512,
#         # need_email=True,
#         # need_phone_number=True,
#         # need_shipping_address=True,
#         # is_flexible=True,  # True If you need to set up Shipping Fee
#         prices=PRICES,
#         start_parameter='time-machine-example',
#         payload='some-invoice-payload-for-our-internal-use'
#     )
#
#
# # @dp.pre_checkout_query_handler(func=lambda query: True)
# # async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
# #     print('order_info')
# #     print(pre_checkout_query.order_info)
# #
# #     if hasattr(pre_checkout_query.order_info, 'email') and (pre_checkout_query.order_info.email == 'vasya@pupkin.com'):
# #         return await bot.answer_pre_checkout_query(
# #             pre_checkout_query.id,
# #             ok=False,
# #             error_message=MESSAGES['wrong_email'])
# #
# #     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#
#
# @router.message(content_types=ContentType.SUCCESSFUL_PAYMENT)
# async def process_successful_payment(message: types.Message):
#     bot = Bot.get_current()
#     await bot.send_message(
#         message.chat.id,
#         'olacheno'
#     )

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from dbcontroller import models
from bot.messages import BotMessages
from config import SessionData


def _is_owner(owner_id):
    owners_ids = models.Owner.select('id')
    if owner_id in owners_ids:
        return True
    return False


def _is_subscriber(sub_id):
    subs_ids = models.Subscriber.select('id')
    if sub_id in subs_ids:
        return True
    return False


class StartMessageMiddleware(BaseMiddleware):
    def __init__(self, session_data: SessionData):
        self.client_session_data = session_data

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        await data['state'].update_data(session_data=self.client_session_data)
        return await handler(event, data)


class OwnerMessageMiddleware(BaseMiddleware):
    def __init__(self, session_data: SessionData):
        self.client_session_data = session_data

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        owner_id = event.from_user.id
        if _is_owner(owner_id):
            await data['state'].update_data(session_data=self.client_session_data)
            return await handler(event, data)

        await event.answer(BotMessages.NO_PERMISSION)


class SubscriberMessageMiddleware(BaseMiddleware):
    def __init__(self, payments_provider_token):
        self.payments_provider_token = payments_provider_token

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        sub_id = event.from_user.id
        if _is_subscriber(sub_id):
            await data['state'].update_data(payments_provider_token=self.payments_provider_token)
            return await handler(event, data)

        await event.answer(BotMessages.NO_PERMISSION)

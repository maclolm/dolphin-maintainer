from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from bot.messages import BotMessages
from config import SessionData
import dbcontroller


def _is_owner(owner_id):
    with dbcontroller.DataBaseController() as db:
        if (owner_id,) in db.get_owner_ids():
            return True
        return False


def _is_subscriber(sub_id):
    with dbcontroller.DataBaseController() as db:
        if (sub_id,) in db.get_sub_ids():
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
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        sub_id = event.from_user.id
        if _is_subscriber(sub_id):
            return await handler(event, data)

        await event.answer(BotMessages.NO_PERMISSION)

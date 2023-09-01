from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
import config


async def get_user_id(username):
    async with TelegramClient(config.session_username, config.api_id, config.api_hash) as client:
        user = await client(GetFullUserRequest(username))
        user_id = user.full_user.id
        return user_id

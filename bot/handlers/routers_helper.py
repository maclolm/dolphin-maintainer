from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from config import Config


async def get_user_id(username):
    async with TelegramClient(Config.session_username, Config.api_id, Config.api_hash) as client:
        user = await client(GetFullUserRequest(username))
        user_id = user.full_user.id
        return user_id

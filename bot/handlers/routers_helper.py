from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
import config


async def get_user_id(username):
    client = TelegramClient(username, config.api_id, config.api_hash)
    user = await client(GetFullUserRequest(username))
    return user
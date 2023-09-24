from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from config import SessionData
from dbcontroller import DataBaseController
from logging import getLogger
log = getLogger('owner_handler')


async def get_username(tg_id, session_data: SessionData):
    async with TelegramClient(
            session_data.session_username,
            session_data.api_id,
            session_data.api_hash) as client:
        user = await client.get_entity(tg_id)
        return user.username


async def get_user_id(username, session_data: SessionData):
    async with TelegramClient(
            session_data.session_username,
            session_data.api_id,
            session_data.api_hash) as client:
        user = await client(GetFullUserRequest(username))
        user_id = user.full_user.id
        return user_id


async def refresh_all_users(db_conn: DataBaseController, session_data: SessionData):
    subs = db_conn.get_all_subs()
    for _, tg_id, username, _, _, _ in subs:
        actual_username = await get_username(tg_id, session_data)
        if username != actual_username:
            db_conn.update_sub_tg_username(tg_id, actual_username)
            log.info(f'Telegram username of sub {username} has been updated [{username}] --> {actual_username}')

    owners = db_conn.get_all_owners()
    for _, tg_id, username in owners:
        actual_username = await get_username(tg_id, session_data)
        if username != actual_username:
            db_conn.update_owner_tg_username(tg_id, actual_username)
            log.info(f'Telegram ID of username {username} has been updated [{username}] --> {actual_username}')



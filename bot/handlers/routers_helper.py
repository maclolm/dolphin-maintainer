from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from config import SessionData
from dbcontroller import DataBaseController
from logging import getLogger
log = getLogger('owner_handler')


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
        actual_tg_id = get_user_id(username, session_data)
        if tg_id != actual_tg_id:
            db_conn.update_sub_tg_id(tg_id, actual_tg_id)
            log.info(f'Telegram ID of sub {username} has been updated [{tg_id}] --> {actual_tg_id}')

    owners = db_conn.get_all_owners()
    for _, tg_id, username in owners:
        actual_tg_id = get_user_id(username, session_data)
        if tg_id != actual_tg_id:
            db_conn.update_owner_tg_id(tg_id, actual_tg_id)
            log.info(f'Telegram ID of owners {username} has been updated [{tg_id}] --> {actual_tg_id}')



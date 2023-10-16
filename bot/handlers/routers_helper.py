import logging

import telethon.errors
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from config import SessionData
from dbcontroller.dbcontroller import DataBaseController
from logging import getLogger
log = getLogger('owner_handler')


async def get_expired_usernames(users: list, session_data: SessionData):
    async with TelegramClient(
            session_data.session_username,
            session_data.api_id,
            session_data.api_hash) as client:
        for tg_id, username in users:
            user = await client.get_entity(tg_id)
            actual_username = "@" + user.username
            if username != actual_username:
                yield tg_id, actual_username


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
        try:
            user = await client(GetFullUserRequest(username))
        except telethon.errors.UsernameInvalidError as ex:
            logging.warning(ex)
            raise
        except ValueError as ex:
            logging.error(ex)
            raise
        user_id = user.full_user.id
        return user_id


async def refresh_all_users(db_conn: DataBaseController, session_data: SessionData):
    subs = db_conn.get_all_subs_usernames()
    subs_with_expired_username = get_expired_usernames(subs, session_data)
    async for tg_id, username in subs_with_expired_username:
        db_conn.update_sub_tg_username(tg_id, username)

    owners = db_conn.get_all_owners_usernames()
    owners_with_expired_username = get_expired_usernames(owners, session_data)
    async for tg_id, username in owners_with_expired_username:
        db_conn.update_sub_tg_username(tg_id, username)

from datatypes import SubStatus


class SQlActions:
    GET_ALL_SUBS = "SELECT * FROM subscribers"
    ADD_TO_SUBS = "INSERT INTO subscribers (tg_id, username, creation_datetime, status, sub_days) " \
                  "VALUES ({user_id:d}, '{username:s}', '{datetime}', {status}, {sub_days:d});"
    DELETE_FROM_SUBS = "DELETE FROM subscribers WHERE tg_id={user_id:d}"
    GET_SUBS_IDS = "SELECT tg_id FROM subscribers;"
    GET_SUB_DAYS = "SELECT sub_days FROM subscribers WHERE tg_id = {tg_id:d};"
    GET_SUB_STATS = "SELECT sub_days, status FROM subscribers WHERE tg_id = '{tg_id:d}';"
    UPDATE_SUB_TG_USERNAME = "UPDATE subscribers SET username = '{actual_username:s}' WHERE tg_id = {tg_id:d}"
    DECREASE_SUB_DAYS = "UPDATE subscribers SET sub_days = sub_days - 1 WHERE sub_days > 0"
    RECALC_SUB_STATUS = "UPDATE subscribers SET status = CASE " \
                        f"WHEN (sub_days = 0) THEN {SubStatus.EXPIRED} " \
                        f"WHEN (sub_days < 3 AND sub_days > 0) THEN {SubStatus.EXPIRED_SOON} END;"
    GET_EXPIRED_SUBS = "SELECT tg_id, sub_days FROM subscribers " \
                       f"WHERE status = {SubStatus.EXPIRED} OR status = {SubStatus.EXPIRED_SOON}"

    ADD_TO_OWNERS = "INSERT INTO owners (tg_id, username) VALUES ({user_id:d}, '{username:s}');"
    DELETE_FROM_OWNERS = "DELETE FROM owners WHERE tg_id={user_id:d}"
    GET_ALL_OWNERS = "SELECT * FROM owners"
    GET_OWNERS_IDS = "SELECT tg_id FROM owners;"
    UPDATE_OWNER_TG_USERNAME = "UPDATE owners SET username = '{actual_username:s}' WHERE tg_id = {tg_id:d}"

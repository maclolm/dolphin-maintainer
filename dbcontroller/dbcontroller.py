import sqlite3
import logging

from datetime import datetime

from .sql_actions import SQlActions
from datatypes import SubStatus

DEFAULT_DB_FILE = 'dolphin-subscribers.db'


class ExistsError(BaseException):
    pass


class DataBaseController:
    def __init__(self, db=DEFAULT_DB_FILE):
        self.conn = sqlite3.connect(db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def __execute_cmd(self, cmd):
        try:
            logging.debug(f'Execute CMD: {cmd}')
            cursor = self.conn.cursor()
            cursor.execute(cmd)
            res = cursor.fetchall()
            if res is None:
                return []
            return res

        except Exception as ex:
            logging.exception(f'Exception while executing cmd {cmd}: {ex}')

    def __execute_and_commit_cmd(self, cmd):
        try:
            self.__execute_cmd(cmd)
            self.conn.commit()
        except Exception as ex:
            logging.exception(f'Exception while commit cmd {cmd}: {ex}')
            self.conn.rollback()

    def init(self):
        try:
            cmd = "CREATE TABLE IF NOT EXISTS subscribers (" \
                  "     id INTEGER PRIMARY KEY," \
                  "     tg_id INT NOT NULL," \
                  "     username CHAR NOT NULL," \
                  "     creation_datetime DATETIME," \
                  "     status INT NOT NULL," \
                  "     sub_days INT" \
                  ");"
            self.__execute_cmd(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS owners (" \
                  "     id INTEGER PRIMARY KEY," \
                  "     tg_id INT NOT NULL," \
                  "     username CHAR NOT NULL" \
                  ");"
            self.__execute_cmd(cmd)

            # TODO: sub_id
            # TODO: или понять что это за дракон https://surik00.gitbooks.io/aiogram-lessons/content/chapter4.html
            cmd = "CREATE TABLE IF NOT EXISTS transactions (" \
                  "     id INTEGER PRIMARY KEY," \
                  "     sub_id CHAR NOT NULL, " \
                  "     amount INT NOT NULL," \
                  "     status INT NOT NULL," \
                  "     date DATETIME" \
                  ");"
            self.__execute_cmd(cmd)

            self.conn.commit()

        except Exception as ex:
            logging.exception(f'Database init error {ex}')
            self.conn.rollback()

    def add_to_sub_table(self, user_id, username, sub_days):
        sql = SQlActions.ADD_TO_SUBS.format(
            user_id=user_id,
            username=username,
            datetime=datetime.now(),
            status=SubStatus.ACTUAL,
            sub_days=int(sub_days)
        )
        self.__execute_and_commit_cmd(sql)

    def add_to_owner_table(self, user_id, username):
        sql = SQlActions.ADD_TO_OWNERS.format(user_id=user_id, username=username)
        self.__execute_and_commit_cmd(sql)

    def delete_from_sub_table(self, user_id):
        sql = SQlActions.DELETE_FROM_SUBS.format(user_id=user_id)
        self.__execute_and_commit_cmd(sql)

    def delete_from_owner_table(self, user_id):
        sql = SQlActions.DELETE_FROM_OWNERS.format(user_id=user_id)
        self.__execute_and_commit_cmd(sql)

    def get_owner_ids(self):
        sql = SQlActions.GET_OWNERS_IDS
        return self.__execute_cmd(sql)

    def get_sub_ids(self):
        sql = SQlActions.GET_SUBS_IDS
        return self.__execute_cmd(sql)

    def get_sub_days(self, tg_id):
        sql = SQlActions.GET_SUB_DAYS.format(tg_id=tg_id)
        (days,) = self.__execute_cmd(sql)[0]
        return days

    def get_sub_stats(self, tg_id):
        sql = SQlActions.GET_SUB_STATS.format(tg_id=tg_id)
        res = self.__execute_cmd(sql)
        if len(res) == 0:
            raise ExistsError()
        (days, status) = res[0]
        return days, status

    def get_all_subs(self):
        sql = SQlActions.GET_ALL_SUBS
        return self.__execute_cmd(sql)

    def get_all_owners(self):
        sql = SQlActions.GET_ALL_OWNERS
        return self.__execute_cmd(sql)

    def get_all_subs_usernames(self):
        sql = SQlActions.GET_SUBS_USERNAMES
        return self.__execute_cmd(sql)

    def get_all_owners_usernames(self):
        sql = SQlActions.GET_OWNERS_USERNAMES
        return self.__execute_cmd(sql)

    def get_expired_subs(self):
        sql = SQlActions.GET_EXPIRED_SUBS
        return self.__execute_cmd(sql)

    def update_sub_tg_username(self, tg_id, actual_username):
        sql = SQlActions.UPDATE_SUB_TG_USERNAME.format(actual_username=actual_username, tg_id=tg_id)
        self.__execute_and_commit_cmd(sql)

    def update_owner_tg_username(self, tg_id, actual_username):
        sql = SQlActions.UPDATE_OWNER_TG_USERNAME.format(actual_username=actual_username, tg_id=tg_id)
        self.__execute_and_commit_cmd(sql)

    def decrease_subscription_days(self):
        sql = SQlActions.DECREASE_SUB_DAYS
        self.__execute_and_commit_cmd(sql)

    def recalc_sub_status(self):
        sql = SQlActions.RECALC_SUB_STATUS
        self.__execute_and_commit_cmd(sql)

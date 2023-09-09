import sqlite3
import logging


class ExistsError(BaseException):
    pass


class DataBaseController:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)

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
                  "     status CHAR NOT NULL," \
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
            cmd = "CREATE TABLE IF NOT EXISTS transactions (" \
                  "     id INTEGER PRIMARY KEY," \
                  "     sub_id CHAR NOT NULL, " \
                  "     amount INT NOT NULL," \
                  "     status CHAR NOT NULL," \
                  "     date DATETIME" \
                  ");"
            self.__execute_cmd(cmd)

            self.conn.commit()

        except Exception as ex:
            logging.exception(f'Database init error {ex}')
            self.conn.rollback()

    def add_to_sub_table(self, user_id, username, sub_days):
        sql = f"INSERT INTO subscribers (tg_id, username, status, sub_days) VALUES ({user_id}, '{username}', '1', {sub_days});"
        self.__execute_and_commit_cmd(sql)

    def add_to_owner_table(self, user_id, username):
        sql = f"INSERT INTO owners (tg_id, username) VALUES ({user_id}, '{username}');"
        self.__execute_and_commit_cmd(sql)

    def delete_from_sub_table(self, user_id):
        sql = f"DELETE FROM subscribers WHERE tg_id={user_id}"
        self.__execute_and_commit_cmd(sql)

    def delete_from_owner_table(self, user_id):
        sql = f"DELETE FROM owners WHERE tg_id={user_id}"
        self.__execute_and_commit_cmd(sql)

    def get_owner_ids(self):
        cmd = "SELECT tg_id FROM owners;"
        return self.__execute_cmd(cmd)

    def get_sub_ids(self):
        cmd = "SELECT tg_id FROM subscribers;"
        return self.__execute_cmd(cmd)

    def get_sub_days(self, tg_id):
        cmd = f"SELECT sub_days FROM subscribers WHERE tg_id = {tg_id};"
        (days,) = self.__execute_cmd(cmd)[0]
        return days

    def get_sub_stats(self, tg_id):
        cmd = f"SELECT sub_days, status FROM subscribers WHERE tg_id = '{tg_id}';"
        res = self.__execute_cmd(cmd)
        if len(res) == 0:
            raise ExistsError()
        (days, status) = res[0]
        return days, status

    def get_all_subs(self):
        cmd = "SELECT * FROM subscribers"
        res = self.__execute_cmd(cmd)
        return res

    def get_expired_subs(self):
        cmd = "SELECT * FROM subscribers WHERE status = '-1'"
        res = self.__execute_cmd(cmd)
        return res

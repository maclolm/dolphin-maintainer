import sqlite3
import logging


class DBcontroller:
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

    def get_expired_subs(self):
        pass

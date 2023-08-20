import sqlite3
import logging


class DBcontroller:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)

    def __execute_cmd(self, cmd):
        cursor = self.conn.cursor()
        cursor.execute(cmd)

    def init(self):
        try:
            cmd = "CREATE TABLE IF NOT EXISTS subscribers (" \
                  "     id INT PRIMARY KEY," \
                  "     tg_username CHAR NOT NULL," \
                  "     status CHAR NOT NULL," \
                  "     sub_days INT" \
                  ");"
            self.__execute_cmd(cmd)

            # TODO: sub_id
            cmd = "CREATE TABLE IF NOT EXISTS transactions (" \
                  "     id INT PRIMARY KEY," \
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

    def get_sub_days(self, username):
        return 0

    def get_owners(self):
        pass

    def get_subs(self):
        pass

    def get_expired_subs(self):
        pass

import datetime
import sqlite3
from datetime import datetime

from src.utils.logger._logger import logger_msg


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)

            print('Подключился к SQL DB:', db_file)

            self.cursor = self.conn.cursor()

            self.check_table()

        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"users (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_user TEXT, "
                                f"username TEXT, "
                                f"first_name TEXT, "
                                f"last_name TEXT, "
                                f"premium TEXT, "
                                f"join_date DATETIME, "
                                f"last_time DATETIME DEFAULT 0, "
                                f"push1 BOOLEAN DEFAULT 0, "
                                f"push2 BOOLEAN DEFAULT 0, "
                                f"push_time DATETIME DEFAULT 0, "
                                f"date_buy DATETIME DEFAULT 0, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table users {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"settings (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"key TEXT, "
                                f"value TEXT)")

        except Exception as es:
            logger_msg(f'SQL исключение check_table settings {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"channels (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"link TEXT, "
                                f"id_chanel TEXT, "
                                f"status BOOLEAN DEFAULT 1, "
                                f"comment TEXT, "
                                f"last_message_id TEXT DEFAULT '[]', "
                                f"count_members TEXT, "
                                f"other TEXT)")

        except Exception as es:
            logger_msg(f'SQL исключение channels {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"words (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"word TEXT, "
                                f"other TEXT)")

        except Exception as es:
            logger_msg(f'SQL исключение words {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"stops (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"word TEXT, "
                                f"other TEXT)")

        except Exception as es:
            logger_msg(f'SQL исключение words {es}')

        return True

    def check_or_add_user(self, id_user, data_user):

        result = self.cursor.execute(f"SELECT * FROM users WHERE id_user='{id_user}'")

        response = result.fetchall()

        if not response:
            now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute("INSERT OR IGNORE INTO users ('id_user', 'username', 'first_name', 'last_name', "
                                "'premium', 'join_date') VALUES (?,?,?,?,?,?)",
                                (id_user, data_user['username'], data_user['first_name'], data_user['last_name'],
                                 data_user['premium'], now_date,))

            self.conn.commit()

            return True

        return False

    def get_all_channels(self):
        try:
            result = self.cursor.execute(f"SELECT * FROM channels "
                                         f"WHERE status = '1'")

            response = result.fetchall()
        except Exception as es:
            error_ = f'SQL ошибка при get_all_channels "{es}"'

            logger_msg(error_)

            return False

        return response

    def get_stop_words(self):
        try:
            result = self.cursor.execute(f"SELECT * FROM stops")

            response = result.fetchall()
        except Exception as es:
            error_ = f'SQL ошибка при get_stop_words "{es}"'

            logger_msg(error_)

            return False

        return response

    def get_words(self):
        try:
            result = self.cursor.execute(f"SELECT word FROM words")

            response = result.fetchall()
        except Exception as es:
            error_ = f'SQL ошибка при get_words "{es}"'

            logger_msg(error_)

            return False

        return response

    def get_words_new(self):
        try:
            result = self.cursor.execute(f"SELECT * FROM words")

            response = result.fetchall()
        except Exception as es:
            error_ = f'SQL ошибка при get_words "{es}"'

            logger_msg(error_)

            return False

        return response

    def get_stops(self):
        try:
            result = self.cursor.execute(f"SELECT word FROM stops")

            response = result.fetchall()
        except Exception as es:
            error_ = f'SQL ошибка при get_stops "{es}"'

            logger_msg(error_)

            return False

        return response

    def edit_user(self, key, value, id_user):

        try:

            result = self.cursor.execute(f"SELECT {key} FROM users "
                                         f"WHERE id_user = '{id_user}'")

            response = result.fetchall()

            if not response:
                logger_msg(f'SQL Не могу отредактировать пользователя "{id_user}" поле: "{key}" значение: "{value}"')
                return False

            self.cursor.execute(f"UPDATE users SET {key} = '{value}' WHERE id_user = '{id_user}'")

            self.conn.commit()

            print(f'SQL: Отредактировал пользователя "{id_user}" поле: "{key}" значение: "{value}"')

            return True

        except Exception as es:
            logger_msg(f'SQL ERROR: Не смог изменить пользователя"{id_user}" поле: "{key}" значение: "{value}" "{es}"')

            return False

    def get_id_by_login(self, username):

        try:

            result = self.cursor.execute(f"SELECT id_user FROM users "
                                         f"WHERE username = '{username}'")

            response = result.fetchall()

            try:
                response = response[0][0]
            except:
                return False

        except Exception as es:
            logger_msg(f'SQL ERROR: при get_id_by_login: "{es}"')

            return False

        return response

    def update_channels(self, id_pk, key, value):

        try:

            self.cursor.execute(f"UPDATE channels SET {key} = '{value}' WHERE id_pk = '{id_pk}'")

            self.conn.commit()

            return True

        except Exception as es:
            logger_msg(f'SQL ERROR при update_channels "{es}"')

            return False

    def get_setting(self, key):

        try:

            result = self.cursor.execute(f"SELECT value FROM settings "
                                         f"WHERE key = '{key}'")

            response = result.fetchall()

            try:
                response = response[0][0]
            except:
                return False

            return response
        except Exception as es:
            logger_msg(f'Ошибка при попытке получить настройку "{key}" "{es}"')

            return False

    def add_channels(self, channels_list):

        try:

            self.cursor.executemany("INSERT INTO channels ('link') VALUES (?)", channels_list)

            self.conn.commit()

        except Exception as es:
            logger_msg(f'SQL ошибка add_channels "{es}"')

            return False

        return True

    def add_words(self, words_list):

        try:

            self.cursor.executemany("INSERT INTO words ('word') VALUES (?)", words_list)

            self.conn.commit()

        except Exception as es:
            logger_msg(f'SQL ошибка add_words "{es}"')

            return False

        return True

    def add_stops(self, words_list):

        try:

            self.cursor.executemany("INSERT INTO stops ('word') VALUES (?)", words_list)

            self.conn.commit()

        except Exception as es:
            logger_msg(f'SQL ошибка add_stops "{es}"')

            return False

        return True

    def start_settings(self, key, value):

        try:

            result = self.cursor.execute(f"SELECT * FROM settings WHERE key='{key}'")

            response = result.fetchall()

            if not response:
                self.cursor.execute("INSERT OR IGNORE INTO settings ('key', 'value') VALUES (?,? )", (key, value))

                self.conn.commit()

                return True

        except Exception as es:
            logger_msg(f'SQL ошибка start_settings "{es}"')

            return False

        return False

    def del_channel(self, id_pk):
        try:

            result = self.cursor.execute(f"DELETE FROM channels WHERE id_pk='{id_pk}'")

            self.conn.commit()

        except Exception as es:
            logger_msg(f'SQL ошибка! При del_channel "{es}"')

            return False

        return True

    def del_word(self, id_pk):
        try:

            result = self.cursor.execute(f"DELETE FROM words WHERE id_pk='{id_pk}'")

            self.conn.commit()

        except Exception as es:
            logger_msg(f'SQL ошибка! При del_word "{es}"')

            return False

        return True

    def del_stop(self, id_pk):
        try:

            result = self.cursor.execute(f"DELETE FROM stops WHERE id_pk='{id_pk}'")

            self.conn.commit()

        except Exception as es:
            logger_msg(f'SQL ошибка! При del_stop "{es}"')

            return False

        return True

    def edit_settings(self, key, value):

        try:

            result = self.cursor.execute(f"SELECT value FROM settings "
                                         f"WHERE key = '{key}'")

            response = result.fetchall()

            if not response:
                self.cursor.execute("INSERT OR IGNORE INTO settings ('key', 'value') VALUES (?,?)",
                                    (key, value))

                self.conn.commit()

                return True

            else:
                self.cursor.execute(f"UPDATE settings SET value = '{value}' WHERE key = '{key}'")

                self.conn.commit()

                return True
        except Exception as es:
            logger_msg(f'Не смог изменить настройку "{key}" "{value}" "{es}"')

            return False

    def close(self):
        self.conn.close()

        print('Отключился от SQL BD')

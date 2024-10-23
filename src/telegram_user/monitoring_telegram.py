import asyncio
import time

from pyrogram import Client

from settings import *

from datetime import datetime

from src.utils.logger._logger import logger_msg


class MonitoringTelegram:
    def __init__(self):

        self.path = sessions_path + f'/{API_ID}'

    async def start_tg(self):

        print(f'{datetime.now().strftime("%H:%M:%S")} Инициализирую вход в аккаунт {API_ID}')

        try:
            self.app = Client(self.path, API_ID, API_HASH, takeout=True, no_updates=True)

            await self.app.start()

        except Exception as es:
            error_ = f'{datetime.now().strftime("%H:%M:%S")} Ошибка при авторизации ({API_ID}) "{es}"'

            logger_msg(error_)

            return False

        return True

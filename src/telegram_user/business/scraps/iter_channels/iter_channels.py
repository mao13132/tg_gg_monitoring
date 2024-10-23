# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
from datetime import datetime

from settings import DEVELOPER
from src.telegram_user.business.scraps.get_id_chat.get_id_chat import GetIdTG
from src.telegram_user.business.scraps.pars_comments.start_pars_comments import StartParsComments
from src.utils.lower_words import lower_words


class IterChannels:
    def __init__(self, settings):
        self.settings = settings

        self.app = settings['app']

        self.BotDB = settings['BotDB']

        self.bot = settings['bot']

    async def start_iter_channels(self, channels_pars):
        # Если нет ключевых слов, то не начинать парсинг
        check_words_list = self.BotDB.get_words()

        if not check_words_list:
            await asyncio.sleep(60)

            return False

        print(f'--- {datetime.now().strftime("%H:%M:%S")} Начало обработки всех каналов\n')

        for count, chanel in enumerate(channels_pars):

            words_list = self.BotDB.get_words()

            if not words_list:
                continue

            stops_list = self.BotDB.get_stops()

            self.settings['words_list'] = await lower_words(words_list)

            self.settings['stops_list'] = await lower_words(stops_list)

            self.settings['channel'] = chanel

            link_chat = chanel[1]

            # ID запрашивать надо каждый раз, как будто идёт первое касание
            settings_get_id = {

                'app': self.app,

                'bot': self.bot,

                'link_chat': link_chat,

            }

            data_chat = await GetIdTG(settings_get_id).get_id_chat()

            if not data_chat:
                continue

            id_chat = data_chat['id_chat']

            type_chat = data_chat['type_chat']

            print(f'\n{count + 1}. {datetime.now().strftime("%H:%M:%S")} Начинаю парсинг чата: {link_chat}\n')

            monitoring_count_task = await StartParsComments(self.settings).start_pars_comments(link_chat, id_chat,
                                                                                               type_chat)

            print(f'\n{count + 1}. {datetime.now().strftime("%H:%M:%S")} Закончил парсинг чата: {link_chat}\n')

            continue

        await asyncio.sleep(200)

        return True

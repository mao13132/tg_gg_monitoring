# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from settings import DEVELOPER
from src.telegram_user.business.scraps.join_chat.join_chat import JoinChatModule
from src.telegram_user.business.scraps.utils.replace_name_channel import replace_name_channel
from src.utils.logger._logger import logger_msg


class GetIdTG:
    def __init__(self, settings):
        self.settings = settings

        self.app = settings['app']

        self.bot = settings['bot']

        self.link_chat = settings['link_chat']

    async def get_id_chat(self):
        name_chat = await replace_name_channel(self.link_chat)

        for _try in range(3):

            try:

                res_chat = await self.app.get_chat(name_chat)

            except Exception as es:
                logger_msg(f'Исключения при получение ID чат {es}')

                if 'FLOOD' in str(es):
                    try:
                        sleep_time = es.value
                    except:
                        sleep_time = 300

                    if sleep_time > 1800:
                        try:
                            await self.bot.send_message(DEVELOPER,
                                                        f'⚠️ Словил FLOOD: {sleep_time} секунд. Останавливаюсь')
                        except:
                            pass

                    try:
                        await asyncio.sleep(sleep_time + 2)
                    except:
                        return False

                    if sleep_time > 1800:
                        try:
                            await self.bot.send_message(DEVELOPER, f'⚠️ Вышел с  FLOOD')
                        except:
                            pass

                    continue

                res_join = await JoinChatModule(self.app).join_to_chat(self.link_chat, self.bot)

                if not res_join:
                    return False

                continue

            try:
                id_chat = res_chat.id

                type_chat = str(res_chat.type).lower()
            except Exception as es:
                logger_msg(f'Ошибка получения id от чата "{es}"')

                if '+' in self.link_chat:
                    res_join = await JoinChatModule(self.app).join_to_chat(self.link_chat, self.bot)

                    if res_join:
                        continue

                return False

            if id_chat is None:
                res_join = await JoinChatModule(self.app).join_to_chat(self.link_chat, self.bot)

                if res_join:
                    continue
                else:
                    return False

            return_dict = {
                'id_chat': id_chat,
                'type_chat': type_chat
            }

            return return_dict

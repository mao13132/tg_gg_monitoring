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
from src.utils.logger._logger import logger_msg


class JoinChatModule:
    def __init__(self, app):
        """@developer_telegrams"""

        self.app = app

    async def join_to_chat(self, name_chat, bot):
        """@developer_telegrams"""
        try:

            response = await self.app.join_chat(name_chat)

        except Exception as es:

            if 'USER_ALREADY_PARTICIPANT' in str(es):
                return True

            if 'FLOOD' in str(es):
                try:
                    await bot.send_message(DEVELOPER, f'⚠️ Словил FLOOD 2: {es.value}')
                except:
                    pass

                try:
                    await asyncio.sleep(es.value + 2)
                except:
                    return False

                try:
                    await bot.send_message(DEVELOPER, f'⚠️ Вышел с  FLOOD 2')
                except:
                    pass

                return True

            if 'INVITE_REQUEST_SENT' in str(es):
                logger_msg(f'Заявку на вступление успешно отправил "{name_chat}"')

                return False

            if 'Username not found' in str(es):
                logger_msg(f'Данный ресурс не доступен "{name_chat}"')

                return False

            if 'INVITE_HASH_EXPIRED' in str(es):
                logger_msg(f'У ссылка вышел срок действия "{name_chat}"')

                return False

            if 'USERNAME_INVALID' in str(es) or 'USERNAME_NOT_OCCUPIED' in str(es):
                logger_msg(f'Чата "{name_chat}" не существует')

                return False

            msg = f'Не могу подписаться на канал "{name_chat}" "{es}"'

            logger_msg(msg)

            return False

        return True

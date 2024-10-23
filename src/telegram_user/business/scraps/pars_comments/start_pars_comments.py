# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.telegram_user.business.scraps.pars_comments._core_comment_pars import CoreCommentsPars
from src.telegram_user.business.scraps.pars_comments._core_messages_pars import CoreMessagesPars
from src.telegram_user.business.scraps.pars_comments._core_theme_chat_pars import CoreThemeChatPars
from src.telegram_user.business.scraps.pars_comments.check_topic_chat import is_topic_chat
from src.utils.logger._logger import logger_msg


class StartParsComments:
    def __init__(self, settings):
        self.settings = settings

        self.app = settings['app']

        self.BotDB = settings['BotDB']

        self.bot = settings['bot']

    async def start_pars_comments(self, link_chat, id_chat, type_chat):

        if 'supergroup' in type_chat:
            is_topics_chat = await is_topic_chat(id_chat, self.app)
        else:
            is_topics_chat = False

        if 'chat' in type_chat and 'channel' not in type_chat and not is_topics_chat:
            # Парсинг по сообщениям
            try:
                count_task = await CoreMessagesPars(self.settings).start_get_messages_members(link_chat, id_chat)
            except Exception as es:
                error_ = f'Ошибка в модуле парсинга по сообщениям в чате "{link_chat}" "{es}"'

                logger_msg(error_)

                return False

            return count_task

        elif is_topics_chat:
            # Парсинг по темам
            try:
                count_task = await CoreThemeChatPars(self.settings).start_get_theme_pars(link_chat, id_chat)
            except Exception as es:
                error_ = f'Ошибка в модуле парсинга по темам в чате "{link_chat}" "{es}"'

                logger_msg(error_)

                return False

            return count_task

        elif 'channel' in type_chat:
            # Парсинг по комментариям
            try:
                count_task = await CoreCommentsPars(self.settings).start_get_comment_members(link_chat, id_chat)
            except Exception as es:
                error_ = f'Ошибка в модуле парсинга по комментариям в чате "{link_chat}" "{es}"'

                logger_msg(error_)

                return False

            return count_task

        else:
            logger_msg(f'Не определен шаблон для работы с "{type_chat}" типом канала/чата')

        return True

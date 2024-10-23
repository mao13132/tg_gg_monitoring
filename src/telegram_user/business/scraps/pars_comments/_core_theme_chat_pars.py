# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from langdetect import detect

from settings import DEEP_SCRAP
from src.business.add_new_msg_sql.add_new_msg_sql import add_new_msg_sql
from src.business.check_old_message.start_check_old_message import start_check_old_message
from src.business.send_message.start_send_message import start_send_message
from src.utils.filter_monitoring_text import filter_monitoring_text


class CoreThemeChatPars:
    def __init__(self, settings):
        self.settings = settings

        self.app = settings['app']

        self.BotDB = settings['BotDB']

        self.bot = settings['bot']

        self.words_list = settings['words_list']

        self.stops_list = settings['stops_list']

    async def start_get_theme_pars(self, link_chat, id_chat):

        add_count = 0

        deep_parsing = DEEP_SCRAP

        deep_parsing = int(deep_parsing)

        async for topic in self.app.get_forum_topics(id_chat):
            all_count = 0

            try:
                id_msg = topic.message_thread_id
            except:
                continue

            async for message in self.app.get_discussion_replies(id_chat, id_msg):
                all_count += 1

                exist = await start_check_old_message(message.id, self.settings['channel'][5])

                if exist:
                    print(f'Все новые сообщения в теме чате "{link_chat}" обработаны')

                    break

                # Первые три сообщения добавляю в sql что бы не обрабатывать их повторно
                if all_count < 3:
                    last_msgs_list = await add_new_msg_sql(message.id, self.settings['channel'], self.BotDB)

                    if last_msgs_list:
                        self.settings['channel'] = list(self.settings['channel'])

                        self.settings['channel'][5] = last_msgs_list

                        self.settings['channel'] = tuple(self.settings['channel'])

                msg_text = message.text if message.text and message.text is not None else message.caption

                try:
                    if msg_text is None:
                        continue
                except:
                    continue

                if all_count >= deep_parsing:
                    print(f'Достиг максимальной глубины парсинга по комментариям "{link_chat}" добавил "{add_count}"')

                    break

                try:
                    msg_text = message.text
                except:
                    continue

                word = await filter_monitoring_text(self.stops_list, self.words_list, msg_text)

                if not word:
                    continue

                try:
                    first_name = message.from_user.first_name if message.from_user.first_name is not None else ''
                except:
                    first_name = ''

                try:
                    last_name = message.from_user.last_name if message.from_user.last_name is not None else ''
                except:
                    last_name = ''

                name = f"{first_name} {last_name}"

                try:
                    get_language = detect(msg_text)
                except:
                    get_language = False

                language = get_language if get_language else '?'

                try:
                    phone = message.from_user.phone_number
                except:
                    phone = ''

                try:
                    premium = 'Да' if message.from_user.is_premium else 'Нет'
                except:
                    premium = 'Нет'

                try:
                    in_date = message.from_user.last_online_date
                except:
                    in_date = False

                try:
                    id_user = str(message.from_user.id)
                except:
                    id_user = ''

                try:
                    username = str(message.from_user.username) if message.from_user.username else ''
                except:
                    username = ''

                try:
                    chat_title = message.chat.title
                except:
                    chat_title = ''

                try:
                    message_date = message.date
                except:
                    message_date = ''

                sql_data = {
                    'search_word': word,
                    'id_user': id_user,
                    'username': username,
                    'full_name': name,
                    'date': message.date,
                    'channel_link': message.link,
                    'id_msg': message.id,
                    'text_msg': msg_text,
                    'language': language,
                    'phone': phone,
                    'premium': premium,
                    'chat_title': chat_title,
                    'message_date': message_date,
                    'link_chat': link_chat,
                }

                if in_date:
                    sql_data['in_date'] = in_date

                res_add = await start_send_message(sql_data, self.bot, self.BotDB)

                if res_add:
                    add_count += 1

                    print(f'Добавил найденное сообщение: "{link_chat}" Найденное ключевое слово: "{word}"')

                print(f'Проверок: "{all_count}" Найдено ключевых слов: "{add_count}""')

        return add_count

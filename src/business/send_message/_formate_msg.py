# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.utils.logger._logger import logger_msg


async def _formate_msg(data_msg):
    user_name = f"<a href='https://t.me/{data_msg['username']}'>@{data_msg['username']}</a>" if data_msg[
        'username'] and data_msg['username'] is not None else 'Скрыт'

    full_name = data_msg['full_name'] if data_msg['full_name'] and data_msg['full_name'] is not None else 'Не указано'

    phone = data_msg['phone'] if data_msg['phone'] and data_msg['phone'] is not None else 'Не указан'

    language = data_msg['language'] if data_msg['language'] else '?'

    try:
        last_online = data_msg['in_date'].strftime('%d-%m-%Y %H:%M:%S')
    except:
        last_online = '?'

    try:
        message_date = data_msg['message_date'].strftime('%d-%m-%Y %H:%M:%S')
    except:
        message_date = 'Не указана'

    try:

        msg = f"📌 Найден ключевое слово <code>{data_msg['search_word']}</code>\n\n" \
              f"Дата написания: <code>{message_date}</code>\n\n" \
              f"Чат: <code>{data_msg['chat_title']}</code>\n\n" \
              f"Подписаться: <a href=''>{data_msg['link_chat']}</a>\n\n" \
              f"Ссылка на сообщение: {data_msg['channel_link']}\n\n" \
              f"Пользователь user_name: {user_name}\n\n" \
              f"ID: <code>{data_msg['id_user']}</code>\n\n" \
              f"Имя полное: <code>{full_name}</code>\n\n" \
              f"Телефон: <code>{phone}</code>\n\n" \
              f"Премиум: <code>{data_msg['premium']}</code>\n\n" \
              f"Язык сообщения: <code>{language}</code>\n\n" \
              f"Последний раз Online: <code>{last_online}</code>\n\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"{data_msg['text_msg']}"
    except Exception as es:
        error_ = f'Ошибка формирования текста "{es}"'

        logger_msg(error_)

        msg = error_

    return msg

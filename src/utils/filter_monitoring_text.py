# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.utils.logger._logger import logger_msg


async def _check_target(words_list, text_msg):
    for word in words_list:
        if word in text_msg:
            return word

    return False


async def _check_stop(stop_list, text_msg):
    for stop in stop_list:
        if stop in text_msg:
            return True

    return False


async def filter_monitoring_text(stops_list, words_list, text_msg):
    if str(text_msg) == 'False' or not text_msg:
        return False

    try:
        lower_msg = text_msg.lower()
    except Exception as es:
        error_ = f'Ошибка при уменьшение регистра текста сообщения "{es}"'

        logger_msg(error_)

        lower_msg = text_msg

    word = await _check_target(words_list, lower_msg)

    if not word:
        return False

    stop_word = await _check_stop(stops_list, lower_msg)

    if stop_word:
        return False
    else:
        return word

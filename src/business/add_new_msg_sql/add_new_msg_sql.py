# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json

from settings import LONG_OLD_MSG_ID
from src.utils.logger._logger import logger_msg


async def add_new_msg_sql(msg_id, sql_row_channel, BotDB):
    try:
        id_pk = sql_row_channel[0]

        last_msgs_list = sql_row_channel[5]

        last_msgs_list = json.loads(last_msgs_list)

        last_msgs_list = sorted(last_msgs_list, key=lambda x: x)

        # Если id сообщений больше 2х то чистим
        if len(last_msgs_list) >= LONG_OLD_MSG_ID:
            last_msgs_list = last_msgs_list[-LONG_OLD_MSG_ID:]

        last_msgs_list.append(str(msg_id))

        last_msgs_list = json.dumps(last_msgs_list)

        res_ = BotDB.update_channels(id_pk=id_pk, key='last_message_id', value=last_msgs_list)

        return last_msgs_list

    except Exception as es:
        error_ = f'Не могу добавить id последнего сообщения в sql "{es}"'

        logger_msg(error_)

        return False

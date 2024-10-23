# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json

from src.utils.logger._logger import logger_msg


async def start_check_old_message(current_msg_id, last_msgs_list):
    try:
        last_msgs_list = json.loads(last_msgs_list)

        if str(current_msg_id) in last_msgs_list:
            return True

        return False
    except Exception as es:
        error_ = f'Не могу проверить id сообщения на обработку "{es}"'

        logger_msg(error_)

        return False

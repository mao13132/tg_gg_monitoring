# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import ADMIN
from src.business.send_message._formate_msg import _formate_msg
from src.business.send_message._send_msg_admins import send_target_msg
from src.business.send_message._get_managers_list import get_managers_list


async def start_send_message(data_msg, bot, BotDB):
    msg = await _formate_msg(data_msg)

    res_send_admins = await send_target_msg(msg, bot, ADMIN)

    managers_list = await get_managers_list(BotDB)

    if managers_list:
        res_send_managers = await send_target_msg(msg, bot, managers_list)

    return True



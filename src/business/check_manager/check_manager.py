# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json

from aiogram.types import Message
from src.telegram.bot_core import BotDB


async def check_manager(message: Message):
    id_user = message.chat.id

    login = message.chat.username

    try:
        login_lower = login.lower()
    except:
        login_lower = login

    managers = BotDB.get_setting('managers')

    if not managers:
        return False

    managers = json.loads(managers)

    if str(id_user) in managers:
        return True

    managers_lower = []

    for manager in managers:
        try:
            managers_lower.append(manager.lower())
        except:
            continue

    if login_lower in managers_lower:
        return True

    return False

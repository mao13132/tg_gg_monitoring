# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json


async def get_managers_list(BotDB):
    managers = BotDB.get_setting('managers')

    if not managers:
        return []

    managers_list = []

    managers = json.loads(managers)

    for manage in managers:

        if manage[:1] == '-':
            if str(manage).isdigit():
                managers_list.append(manage)

                continue

        # Если добавлен ник
        if str(manage).isdigit():
            managers_list.append(manage)

            continue

        id_user = BotDB.get_id_by_login(manage)

        if id_user:
            managers_list.append(id_user)

        continue

    return managers_list

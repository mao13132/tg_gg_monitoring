# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from src.utils.logger._logger import logger_msg


async def send_target_msg(msg, bot, users_list):
    for user_ in users_list:

        if len(msg) > 4096:
            for x in range(0, len(msg), 4096):
                try:
                    await bot.send_message(user_, msg[x:x + 4096], disable_web_page_preview=True)
                except Exception as es:
                    if str(es) == 'Chat not found':
                        break

                    error_ = f'Ошибка при отправке целевого сообщения ({user_}) "{es}"'

                    logger_msg(error_)

                    break
        else:
            # Две попытки, для флуда
            for _try in range(2):

                try:
                    await bot.send_message(user_, msg, disable_web_page_preview=True)

                    break
                except Exception as es:
                    if str(es) == 'Chat not found':
                        break

                    if 'Flood' in str(es):
                        try:
                            sleep = [int(row) for row in str(es).split() if str(row).isdigit()][0]
                        except:
                            sleep = 60

                        await asyncio.sleep(sleep + 1)

                        # Пробую ещё раз отправить
                        continue

                    error_ = f'Ошибка при отправке целевого сообщения 2 ({user_}) "{es}"'

                    logger_msg(error_)

                    break

    return True

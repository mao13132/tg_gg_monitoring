# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import LOGO, START_MESSAGE, ADMIN
from src.business.check_manager.check_manager import check_manager
from src.business.get_data_user.get_data_user import get_data_user
from src.telegram.keyboard.keyboards import Admin_keyb

from src.telegram.sendler.sendler import Sendler_msg

from aiogram.types import Message, ChatActions

from src.telegram.bot_core import BotDB

from aiogram.dispatcher import FSMContext


async def start_one(message: Message, state: FSMContext):
    await state.finish()

    try:
        await message.bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    except:
        pass

    id_user = message.chat.id

    data_user = await get_data_user(message)

    new_user = BotDB.check_or_add_user(id_user, data_user)

    is_manager = await check_manager(message)

    if not is_manager and str(id_user) not in ADMIN:
        await Sendler_msg.sendler_photo_message(message, LOGO, '❌ В доступе отказано', None)

        return False

    await Sendler_msg.log_client_message(message)

    keyb = Admin_keyb().start_keyb()

    await Sendler_msg().sendler_photo_message(message, LOGO, START_MESSAGE, keyb)

    return True

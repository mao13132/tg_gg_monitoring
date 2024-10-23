import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from aiogram import Dispatcher

from settings import LOGO
from src.business.start_one.start_one import start_one

from src.telegram.bot_core import BotDB
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg


async def start(message: Message, state: FSMContext):
    await state.finish()

    result = await start_one(message, state)

    return result


async def del_(message: Message):
    try:
        id_channel = str(message.text).split('_')[1]
    except Exception as es:
        msg = f'Ошибка при разборе для удаления del_{es}'

        return False

    _del_word = BotDB.del_channel(id_channel)

    if _del_word:
        _msg = f'✅ Канал удален'
    else:
        _msg = f'❌ Ошибка удаления канала'

    keyb = Admin_keyb().back_add_channels()

    await Sendler_msg().new_sendler_photo_message(message, LOGO, _msg, keyb)

    return True


async def dels_(message: Message):
    try:
        manager = str(message.text).split('_')[1]
    except Exception as es:
        msg = f'Ошибка при разборе для удаления dels_{es}'

        return False

    managers = BotDB.get_setting('managers')

    managers = json.loads(managers)

    res_ = managers.remove(manager)

    managers_sql = json.dumps(managers)

    res_update = BotDB.edit_settings(key='managers', value=managers_sql)

    if res_update:
        status_remove = f'✅ Менеджер удален\n\n'
    else:
        status_remove = f'❌ Ошибка удаления менеджер\n\n'

    if managers_sql:
        msg = f'{status_remove}<b>Список менеджеров:</b>\n\n'
    else:
        msg = f'{status_remove}❌<b>Список менеджеров пуст</b>'

    msg += f'\n'.join(f'{count + 1}. {manager} - Удалить '
                      f'/dels_{manager}' for count, manager in enumerate(managers))

    keyb = Admin_keyb().managers()

    await Sendler_msg().new_sendler_photo_message(message, LOGO, msg, keyb)

    return True


async def delw_(message: Message):
    try:
        id_word = str(message.text).split('_')[1]
    except Exception as es:
        msg = f'Ошибка при разборе для удаления delw_ {es}'

        return False

    _del_word = BotDB.del_word(id_word)

    if _del_word:
        _msg = f'✅ Слово удалено'
    else:
        _msg = f'❌ Ошибка удаления слова'

    keyb = Admin_keyb().back_add_words()

    await Sendler_msg().new_sendler_photo_message(message, LOGO, _msg, keyb)

    return True


async def delp_(message: Message):
    try:
        id_word = str(message.text).split('_')[1]
    except Exception as es:
        msg = f'Ошибка при разборе для удаления delp_ {es}'

        return False

    _del_word = BotDB.del_stop(id_word)

    if _del_word:
        _msg = f'✅ Слово удалено'
    else:
        _msg = f'❌ Ошибка удаления слова'

    keyb = Admin_keyb().back_add_stops()

    await Sendler_msg().new_sendler_photo_message(message, LOGO, _msg, keyb)

    return True


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start', state='*')

    dp.register_message_handler(del_, text_contains='/del_')

    dp.register_message_handler(dels_, text_contains='/dels_')

    dp.register_message_handler(delw_, text_contains='/delw_')

    dp.register_message_handler(delp_, text_contains='/delp_')

    dp.register_message_handler(start, text_contains='')

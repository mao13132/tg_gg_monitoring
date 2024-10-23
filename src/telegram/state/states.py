import json

from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from settings import LOGO
from src.business.utils.scrap_add_channels import scrap_add_channels
from src.telegram.devision_msg.devision_msg import division_message
from src.telegram.keyboard.keyboards import Admin_keyb

from src.telegram.bot_core import BotDB
from src.telegram.sendler.sendler import Sendler_msg
from src.utils.filter_add_words import filter_add_words


class States(StatesGroup):
    test = State()

    add_channels = State()

    add_manager = State()

    add_words = State()

    add_stops = State()


async def add_channels(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    _channels_list = message.text

    channels_list = await scrap_add_channels(_channels_list)

    if not channels_list:
        keyb = Admin_keyb().back_add_channels()

        error = f'⚠️ Вы не верно указали канал(ы). Попробуйте ещё раз'

        await Sendler_msg().sendler_photo_message(message, LOGO, error, keyb)

        return False

    query_sql_channels = [(channel,) for channel in channels_list]

    res_add = BotDB.add_channels(query_sql_channels)

    channels_text = "\n".join(f"<b>{link}</b>" for link in channels_list)

    _msg = f'✅ <b>Канал(ы) успешно добавлены:</b>' \
           f'\n\n{channels_text}'

    keyb = Admin_keyb().back_add_channels()

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_message(message, LOGO, _msg, keyb)
    else:
        await division_message(message, _msg, keyb)

    await state.finish()


async def add_manager(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    manager = message.text

    if '@' in manager:
        manager = manager.replace('@', '')

    try:
        manager = manager.lower()
    except:
        pass

    managers = BotDB.get_setting('managers')

    if managers:
        managers = json.loads(managers)
    else:
        managers = []

    managers.append(manager)

    managers = list(set(managers))

    managers_sql = json.dumps(managers)

    res_update = BotDB.edit_settings(key='managers', value=managers_sql)

    status_add = f'✅ {manager} успешно добавлен\n\n' if res_update else f'❌ Не смог добавить {manager}\n\n'

    _msg = f'{status_add}<b>Список менеджеров:</b>\n\n'

    _msg += f'\n'.join(f'{count + 1}. {manager} - Удалить '
                       f'/dels_{manager}' for count, manager in enumerate(managers))

    keyb = Admin_keyb().managers()

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_message(message, LOGO, _msg, keyb)
    else:
        await division_message(message, _msg, keyb)

    return True


async def add_words(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    _channels_list = message.text

    channels_list = await filter_add_words(_channels_list)

    keyb = Admin_keyb().back_add_words()

    if not channels_list:
        error = f'⚠️ Вы не верно указали ключевые слово(а). Попробуйте ещё раз'

        await Sendler_msg().sendler_photo_message(message, LOGO, error, keyb)

        return False

    query_sql_channels = [(channel,) for channel in channels_list]

    res_add = BotDB.add_words(query_sql_channels)

    channels_text = "\n".join(f"<b>{word}</b>" for word in channels_list)

    _msg = f'✅ <b>Слово(а) успешно добавлены:</b>' \
           f'\n\n{channels_text}'

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_message(message, LOGO, _msg, keyb)
    else:
        await division_message(message, _msg, keyb)

    await state.finish()


async def add_stops(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    _channels_list = message.text

    channels_list = await filter_add_words(_channels_list)

    keyb = Admin_keyb().back_add_stops()

    if not channels_list:
        error = f'⚠️ Вы не верно указали стоп слово(а). Попробуйте ещё раз'

        await Sendler_msg().sendler_photo_message(message, LOGO, error, keyb)

        return False

    query_sql_channels = [(channel,) for channel in channels_list]

    res_add = BotDB.add_stops(query_sql_channels)

    channels_text = "\n".join(f"<b>{word}</b>" for word in channels_list)

    _msg = f'✅ <b>Слово(а) успешно добавлены:</b>' \
           f'\n\n{channels_text}'

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_message(message, LOGO, _msg, keyb)
    else:
        await division_message(message, _msg, keyb)

    await state.finish()


def register_state(dp: Dispatcher):
    dp.register_message_handler(add_channels, state=States.add_channels)

    dp.register_message_handler(add_manager, state=States.add_manager)

    dp.register_message_handler(add_words, state=States.add_words)

    dp.register_message_handler(add_stops, state=States.add_stops)

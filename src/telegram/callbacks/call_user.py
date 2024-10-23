import json

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from settings import LOGO
from src.business.check_manager.check_manager import check_manager
from src.business.start_one.start_one import start_one
from src.telegram.devision_msg.devision_msg import division_message
from src.telegram.sendler.sendler import *

from src.telegram.keyboard.keyboards import *
from src.telegram.state.states import States


async def over_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await Sendler_msg.log_client_call(call)

    await start_one(call.message, state)

    return True


async def channels(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    id_user = call.message.chat.id

    is_manager = await check_manager(call.message)

    if not is_manager and str(id_user) not in ADMIN:
        return False

    keyb = Admin_keyb().channels()

    channel_list = BotDB.get_all_channels()

    if not channel_list:
        _msg = '⛔️ Список каналов пуст'

        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

        return False

    _msg = '<b>Список каналов:</b>\n\n'

    _msg += f'\n'.join(f'{count + 1}. {channel[1]} - Удалить '
                       f'/del_{channel[0]}' for count, channel in enumerate(channel_list))

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)
    else:
        await division_message(call.message, _msg, keyb)

    return True


async def add_channel(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    id_user = call.message.chat.id

    _msg = f'<b>Укажите список Каналов</b>\n\n' \
           f'Можете указывать сразу несколько\n' \
           f'разделять пробелом, запятой или переносом строки'

    keyb = Admin_keyb().back_add_channels()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_channels.set()

    return True


async def admin_panel(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    is_manager = await check_manager(call.message)

    id_user = call.message.chat.id

    if not is_manager and str(id_user) not in ADMIN:
        return False

    keyb = Admin_keyb().admin_panel(is_manager)

    msg = f'Вы находитесь в админ панели'

    await Sendler_msg().sendler_photo_call(call, LOGO, msg, keyb)

    return True


async def managers(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    id_user = call.message.chat.id

    keyb = Admin_keyb().managers()

    managers = BotDB.get_setting('managers')

    if managers:
        managers = json.loads(managers)

    if not managers:
        _msg = '⛔️ Список менеджеров пуст'

        await Sendler_msg.send_msg_call(call, _msg, keyb)

        return False

    _msg = '<b>Список менеджеров:</b>\n\n'

    _msg += f'\n'.join(f'{count + 1}. {manager} - Удалить '
                       f'/dels_{manager}' for count, manager in enumerate(managers))

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)
    else:
        await division_message(call.message, _msg, keyb)

    return True


async def add_managers(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    id_user = call.message.chat.id

    _msg = f'Укажите телеграм ник или ID телеграмма менеджера'

    keyb = Admin_keyb().back_managers()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_manager.set()

    return True


async def words(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    id_user = call.message.chat.id

    is_manager = await check_manager(call.message)

    if not is_manager and str(id_user) not in ADMIN:
        return False

    keyb = Admin_keyb().words()

    word_list = BotDB.get_words_new()

    if not word_list:
        _msg = '⛔️ Список ключевых слов пуст'

        await Sendler_msg.send_msg_call(call, _msg, keyb)

        return False

    _msg = '<b>Список ключевых слов:</b>\n\n'

    _msg += f'\n'.join(f'{count + 1}. {word[1]} - Удалить '
                       f'/delw_{word[0]}' for count, word in enumerate(word_list))

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)
    else:
        await division_message(call.message, _msg, keyb)

    return True


async def add_word(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    id_user = call.message.chat.id

    _msg = f'<b>Укажите список ключевых слов</b>\n\n' \
           f'Можете указывать сразу несколько\n' \
           f'разделять или переносом строки\n' \
           f'Регист не важен'

    keyb = Admin_keyb().back_add_words()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_words.set()

    return True


async def stops(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    id_user = call.message.chat.id

    is_manager = await check_manager(call.message)

    if not is_manager and str(id_user) not in ADMIN:
        return False

    keyb = Admin_keyb().stops()

    stop_word_list = BotDB.get_stop_words()

    if not stop_word_list:
        _msg = '⛔️ Список стоп слов пуст'

        await Sendler_msg.send_msg_call(call, _msg, keyb)

        return False

    _msg = '<b>Список стоп слов:</b>\n\n'

    _msg += f'\n'.join(f'{count + 1}. {word[1]} - Удалить '
                       f'/delp_{word[0]}' for count, word in enumerate(stop_word_list))

    if len(_msg) < 1024:
        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)
    else:
        await division_message(call.message, _msg, keyb)

    return True


async def add_stop(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    id_user = call.message.chat.id

    _msg = f'<b>Укажите список стоп слов</b>\n\n' \
           f'Можете указывать сразу несколько\n' \
           f'разделять или переносом строки\n' \
           f'Регистр не важен'

    keyb = Admin_keyb().back_add_stops()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_stops.set()

    return True


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(channels, text='channels', state='*')

    dp.register_callback_query_handler(over_state, text='over_state', state='*')

    dp.register_callback_query_handler(add_channel, text='add_channels', state='*')

    dp.register_callback_query_handler(admin_panel, text='admin_panel', state='*')

    dp.register_callback_query_handler(managers, text='managers', state='*')

    dp.register_callback_query_handler(add_managers, text='add_managers', state='*')

    dp.register_callback_query_handler(words, text='words', state='*')

    dp.register_callback_query_handler(add_word, text='add_word', state='*')

    dp.register_callback_query_handler(stops, text='stops', state='*')

    dp.register_callback_query_handler(add_stop, text='add_stop', state='*')

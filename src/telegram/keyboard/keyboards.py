from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class Admin_keyb:
    def start_keyb(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'📋 Ссылки на мониторинг', callback_data='channels'))

        self._start_key.add(InlineKeyboardButton(text=f'👨‍💻 Админ панель', callback_data='admin_panel'))

        return self._start_key

    def channels(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'➕ Добавить канал', callback_data=f'add_channels'))

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='over_state'))

        return core_keyb

    def back_add_channels(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'channels'))

        return core_keyb

    def words(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'➕ Добавить ключевое слово', callback_data=f'add_word'))

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='admin_panel'))

        return core_keyb

    def admin_panel(self, is_manager):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        if not is_manager:
            self._start_key.add(InlineKeyboardButton(text=f'📎 Менеджеры', callback_data='managers'))

        self._start_key.add(InlineKeyboardButton(text=f'🔍 Ключевые слова', callback_data='words'))

        self._start_key.add(InlineKeyboardButton(text=f'❌ Стоп слова', callback_data='stops'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='over_state'))

        return self._start_key

    def managers(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'➕ Добавить менеджера', callback_data='add_managers'))

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='admin_panel'))

        return core_keyb

    def back_admin(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='admin_panel'))

        return self._start_key

    def back_managers(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='managers'))

        return self._start_key

    def back_add_words(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'words'))

        return core_keyb

    def stops(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'➕ Добавить стоп слово', callback_data=f'add_stop'))

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='admin_panel'))

        return core_keyb

    def back_add_stops(self):
        core_keyb = InlineKeyboardMarkup(row_width=1)

        core_keyb.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'stops'))

        return core_keyb

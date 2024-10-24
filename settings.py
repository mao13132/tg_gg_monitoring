import os

from dotenv import load_dotenv

project_path = os.path.dirname(__file__)

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

sessions_path = os.path.join(os.path.dirname(__file__), 'src', 'telegram_user', 'sessions')

load_dotenv(dotenv_path)

# Сколько старых ID от сообщений держать в истории
LONG_OLD_MSG_ID = 50

DEVELOPER = 5982144791

ADMIN = ['5982144791']

TOKEN = os.getenv('TOKEN')

API_ID = os.getenv('API_ID')

API_HASH = os.getenv('API_HASH')

START_MESSAGE = 'Меню бота для поиска клиентов'

LOGO = r'src/telegram/media/logo.jpg'

LOGGER = True

DEEP_SCRAP = 50

ONE_START = False

MOKE_TG_USER = False

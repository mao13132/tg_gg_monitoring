import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings import MOKE_TG_USER
from src.business.schedule.start_schedule_scrap import StartScheduleScrap
from src.business.start_sql_data.start_sql_data import start_sql_data
from src.telegram.bot_core import *
from src.telegram.handlers.users import *
from src.telegram.state.states import *
from src.telegram.callbacks.call_user import *
from src.telegram_user.monitoring_telegram import MonitoringTelegram


def registration_all_handlers(dp):
    register_user(dp)


def registration_state(dp):
    register_state(dp)


def registration_calls(dp):
    register_callbacks(dp)


async def main():
    bot_start = Core()

    start_data = await start_sql_data(bot_start.BotDB)

    if not MOKE_TG_USER:
        bot_user_core = MonitoringTelegram()

        res_auth = await bot_user_core.start_tg()

        if not res_auth:
            return False

        print(f'Успешно подключился к Telegram начал работу')

    registration_state(bot_start.dp)
    registration_calls(bot_start.dp)
    registration_all_handlers(bot_start.dp)

    scheduler = AsyncIOScheduler()

    if not MOKE_TG_USER:
        settings_schedule = {
            'app': bot_user_core.app,
            'BotDB': bot_start.BotDB,
            'bot': bot_start.bot,
        }

        scheduler.add_job(StartScheduleScrap(settings_schedule).check_scheduler, 'interval', seconds=1)

    scheduler.start()

    try:
        await bot_start.dp.start_polling()
    finally:
        await bot_start.dp.storage.close()
        await bot_start.dp.storage.wait_closed()
        await bot_start.bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(f'Бот остановлен!')

# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime

from src.telegram_user.business.scraps.start_scraps import Scraps


class StartScheduleScrap:
    def __init__(self, settings):
        self.settings = settings

        self.app = settings['app']

        self.BotDB = settings['BotDB']

        self.bot = settings['bot']

    async def check_scheduler(self):
        res_ = await Scraps(self.settings).start_scraps()

        return res_

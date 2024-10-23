# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from src.telegram_user.business.scraps.iter_channels.iter_channels import IterChannels


class Scraps:
    def __init__(self, settings):
        self.settings = settings

        self.app = settings['app']

        self.BotDB = settings['BotDB']

        self.bot = settings['bot']

    async def start_scraps(self):
        channels_from_parsing = self.BotDB.get_all_channels()

        if not channels_from_parsing:
            print(f'Нет каналов на мониторинг')

            await asyncio.sleep(60)

            return False

        channels_from_parsing = sorted(channels_from_parsing, reverse=True)

        res_parsing = await IterChannels(self.settings).start_iter_channels(channels_from_parsing)

        return res_parsing

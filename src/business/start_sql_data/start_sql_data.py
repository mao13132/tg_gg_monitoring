# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import ONE_START
from src.business.start_sql_data.blacks_words import blacks_words_list
from src.business.start_sql_data.channels_start import channels_start_list
from src.business.start_sql_data.words import words_list


async def start_sql_data(BotDB):

    if ONE_START:

        res_ = BotDB.start_settings(key='deep_parsing', value='500')

        res_ = BotDB.start_settings(key='managers', value='["neo_simpson"]')

        res_ = BotDB.start_settings(key='time_send', value='60')

        channels_sql = [(link, ) for link in channels_start_list.split('\n') if link]

        res_add = BotDB.add_channels(channels_sql)

        words = [(word, ) for word in words_list.split('\n') if word]

        res_add = BotDB.add_words(words)

        blacks = [(black, ) for black in blacks_words_list.split('\n') if black]

        res_add = BotDB.add_stops(blacks)

    return True

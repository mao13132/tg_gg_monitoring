# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

sep_list = ['\n', ',', ';']


async def filter_add_words(word_list):
    for _sep in sep_list:
        if _sep in word_list:
            temp_list = [x.strip() for x in word_list.split(_sep) if x != '']
            return set(temp_list)

    return [word_list]

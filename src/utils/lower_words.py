# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
async def lower_words(word_list):
    good_list = []

    for row in word_list:
        try:
            word = row[0].lower()
        except:
            continue

        good_list.append(word)

    return good_list

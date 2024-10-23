# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
async def is_topic_chat(id_chat, app):
    try:
        async for topic in app.get_forum_topics(id_chat):
            return True
    except:
        return False

from hydrogram import Client, filters


@Client.on_message(filters.chat("writer_debug_group"), group=3)
def catch_all(c, m):
    m.reply(f"```json\n{m}```")

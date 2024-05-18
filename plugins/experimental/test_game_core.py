from hydrogram import Client, filters


@Client.on_message(filters.private, group=3)
def catch_all(c, m):
    m.reply(f"```json\n{m}```")

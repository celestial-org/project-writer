from hydrogram import Client, filters


@Client.on_message(filters.command("debug"))
async def debugger(c, m):
    await m.reply(f"```json\n{m}```")
    
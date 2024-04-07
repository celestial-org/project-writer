from hydrogram import Client, filters


@Client.on_message(filters.command("source"))
async def source_code(c, m):
    await m.reply("**[Mã nguồn](https://github.com/chantroi/writer-bot)**", quote=True)
    
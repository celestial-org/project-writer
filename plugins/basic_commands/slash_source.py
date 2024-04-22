from hydrogram import Client, filters


@Client.on_message(filters.command("source"))
def soiIurce_code(c, m):
    m.reply("**[Mã nguồn](https://github.com/chantroi/writer-bot)**", quote=True)

from hydrogram import Client, filters

@Client.on_message(filters.command("source"))
def source_code(c, m):
    m.reply("**[Source](https://github.com/chantroi/writer-bot)**", quote=True)
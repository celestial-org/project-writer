from hydrogram import Client, filters


@Client.on_message(filters.command("debug"))
def debugger(c, m):
    m.reply(f"```json\n{m}```")


@Client.on_message(filters.command("parse"))
def test_parse_mode(c, m):
    text = m.text.split(" ", 1)[1]
    m.reply(text)
    m.delete()

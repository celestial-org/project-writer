from pyrogram import Client, filters


@Client.on_message(filters.command("debug"))
async def debugger(c, m):
    await m.reply(f"```json\n{m}```")


@Client.on_message(filters.command("parse"))
async def test_parse_mode(c, m):
    text = m.text.split(" ", 1)[1]
    await m.reply(text)
    await m.delete()

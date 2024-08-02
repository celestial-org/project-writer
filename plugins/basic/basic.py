import aiofiles as fs
from pyrogram import Client, filters
from pyrogram.enums import ChatAction


@Client.on_message(filters.command(["start", "help"]))
async def send_welcome(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply(
        f"Xin chào {m.from_user.first_name}(`{m.from_user.id}`)",
        quote=True,
    )


@Client.on_message(filters.command("helps"))
async def help_list(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    async with fs.open("text/helps.md", encoding="utf-8") as f:
        text = await f.read()
    text = text.replace("{first_name}", m.from_user.first_name)
    text = text.replace("{uid}", str(m.from_user.id))
    await m.reply(text, quote=True)


@Client.on_message(filters.command("ext"))
async def ext_command_list(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    async with fs.open("text/ext.md", encoding="utf-8") as f:
        text = await f.read()
    text = text.replace("{first_name}", m.from_user.first_name)
    text = text.replace("{uid}", str(m.from_user.id))
    await m.reply(text, quote=True)

import os
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from database import Options

owner = int(os.getenv("OWNER_ID"))


@Client.on_message(filters.command("set_interval"))
def set_interval(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if m.from_user.id != owner:
        m.reply("You don't have permission to use this command", quote=True)
        return
    if len(m.command) > 1:
        interval = m.command[1]
        db = Options()
        db.set_option("interval", interval)
    else:
        m.reply("Please specify an interval", quote=True)

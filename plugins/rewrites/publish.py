import re

from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from deta import Deta




@Client.on_message(filters.command("publish"))
def publish(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    deta = Deta()
    db = deta.Base("reverse")
    link = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        m.text,
    )
    if not link:
        m.reply("Vui long nhap link", quote=True)
        return
    link_id = generate_id()
    db.put({"key": link_id, "target": link})
    m.reply(f"Link: {link[0]}\nLink id: {link_id}", quote=True)

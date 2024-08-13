import os
import sys
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from boot import kv


def is_owner(_, __, m):
    return m.from_user.id in kv["owners"]


@Client.on_message(filters.command("reset") & filters.create(is_owner))
def reset_program(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    md = m.reply("Đang khởi động lại chương trình Client...")
    with open("reset.txt", "w", encoding="utf-8") as f:
        f.write(str(m.chat.id) + ":" + str(md.id))
    os.execl(sys.executable, sys.executable, *sys.argv)

import os
import sys

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from .admin import admin


@Client.on_message(filters.command("reset") & filters.user(admin))
def reset_program(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    md = m.reply("Đang khởi động lại chương trình Client...")
    with open("reset.txt", "w") as f:
        f.write(str(m.chat.id) + ":" + str(md.id))
    os.execl(sys.executable, sys.executable, *sys.argv)

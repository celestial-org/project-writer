import os
import sys
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from .admin import admin


@Client.on_message(filters.command("update") & filters.user(admin))
def update_server(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    mp = m.reply("Đang cập nhật hệ thống...")
    os.system("git stash")
    os.system("git pull")
    md = m.reply("Đã cập nhật xong đang khởi động lại...")
    mp.delete()
    with open("reset.txt", "w") as f:
        f.write(str(m.chat.id) + ":" + str(md.id))
    os.execl(sys.executable, sys.executable, *sys.argv)

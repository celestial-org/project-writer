from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from .admin import admin
import os
import sys


@Client.on_message(filters.command("update") & filters.user(admin))
async def update_server(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply("Đang cập nhật hệ thống...")
    os.system("git config --global pull.rebase true")
    os.system('git config --global user.name "Writer"')
    os.system('git config --global user.email "duongchantroi@alwaysdata.net"')
    os.system("git config --global pull.rebase true")
    os.system("git add * && git commit -a -m UPDATE")
    os.system("git pull")
    m.reply("Đã cập nhật xong đang khởi động lại...")
    with open("reset.txt", "w") as f:
        f.write(str(m.chat.id))
    os.execl(sys.executable, sys.executable, *sys.argv)

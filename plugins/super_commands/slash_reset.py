from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from .admin import admin
import os
import sys


@Client.on_message(filters.command("reset") & filters.user(admin))
async def reset_program(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply("Đang khởi động lại chương trình Client...")
    with open("reset.txt", "w") as f:
        f.write(str(m.chat.id))
    os.execl(sys.executable, sys.executable, *sys.argv)

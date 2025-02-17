import os
import sys
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from sub_task import kv


def is_owner(_, __, m):
    return m.from_user.id in kv.get("owners")


@Client.on_message(filters.command("update_system") & filters.create(is_owner))
def update_server(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    mp = m.reply("Đang cập nhật hệ thống...")
    os.system("git stash")
    os.system("git pull")
    md = m.reply("Đã cập nhật xong đang khởi động lại...")
    mp.delete()
    with open("reset.txt", "w", encoding="utf-8") as f:
        f.write(str(m.chat.id) + ":" + str(md.id))
    os.execl(sys.executable, sys.executable, *sys.argv)

from pyrogram import Client, filters
import os, sys, requests

@Client.on_message(filters.command("reset") & filters.user(5665225938))
def reset_program(c, m):
    m.reply("Đang khởi động lại chương trình Client...")
    with open("reset.txt", "w") as f:
        f.write(str(m.chat.id))
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("resetapi") & filters.user(5665225938))
def reset_api_server(c, m):
    requests.post(f"{server_test}/reset")
    m.reply("Đã gửi lệnh khởi động lại API", quote=True)
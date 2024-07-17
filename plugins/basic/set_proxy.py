import os
import time
from pyrogram import Client, filters
from database import Options


@Client.on_message(filters.command("set_proxy"))
def set_proxy(c, m):
    proxy = m.command[1]
    os.system("pkill -9 lite")
    os.system(f"./lite -p 6868 {proxy} &")
    stt = m.reply("Đã thiết lập proxy")
    m.delete()
    time.sleep(10)
    stt.delete()
    os.environ["http_proxy"] = os.environ["https_proxy"] = "http://127.0.0.1:6868"
    db = Options()
    db.set_option("proxy", proxy)

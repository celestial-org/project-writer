import os
import time
from hydrogram import Client, filters


@Client.on_message(filters.command("set_proxy") & filters.user(5665225938))
def set_proxy(c, m):
    proxy = m.command[1]
    os.system("pkill -9 lite")
    os.system(f"./lite -p 6868 {proxy} &")
    stt = m.reply("Đã thiết lập proxy")
    m.delete()
    time.sleep(10)
    stt.delete()
from hydrogram import Client, filters
import os

@Client.on_message(filters.command("set_proxy") & filters.user(5665225938))
def set_proxy(c, m):
    proxy = m.command[1]
    os.system("killall -9 lite")
    os.system(f"./lite -p 3333 {proxy} &")
    m.reply("Đã thiết lập proxy")
    m.delete()
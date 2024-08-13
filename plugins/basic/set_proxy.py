import time
from pyrogram import Client, filters
from data import Database
from utils.set_proxy import set_proxy


@Client.on_message(filters.command("proxy"))
def set_proxy_command(c, m):
    proxy = m.command[1]
    set_proxy(proxy)
    stt = m.reply("Đã thiết lập proxy")
    m.delete()
    time.sleep(10)
    stt.delete()
    db = Database()
    db.add_preset("proxy", proxy)

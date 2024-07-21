import time
from pyrogram import Client, filters
from database import Options
from assets.note_util import set_proxy


@Client.on_message(filters.command("proxy"))
def set_proxy_command(c, m):
    proxy = m.command[1]
    set_proxy(proxy)
    stt = m.reply("Đã thiết lập proxy")
    m.delete()
    time.sleep(10)
    stt.delete()
    db = Options()
    db.set_option("proxy", proxy)

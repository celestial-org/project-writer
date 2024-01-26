from hydrogram import Client, filters
import subprocess

@Client.on_message(filters.command("set_proxy") & filters.user(5665225938))
def set_proxy(c, m):
    proxy = m.command[1]
    subprocess.run(["./lite", proxy, "&"], shell=True)
    m.reply("Đã thiết lập proxy")
    m.delete()
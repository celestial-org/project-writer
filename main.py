import os, sys, requests
from pyrogram import Client, filters, idle
from lib.env import tokens, config_tool, server_test

bot = Client("writer",
             tokens()[0],
             tokens()[1],
             bot_token=tokens()[2],
             plugins={"root": "plugins"})
             
@bot.on_message(filters.command("reset") & filters.user(5665225938))
def reset_program(c, m):
    m.reply("Đang khởi động lại chương trình bot...")
    with open("reset.txt", "w") as f:
        f.write(str(m.chat.id))
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("resetapi") & filters.user(5665225938))
def fix_api_server(c, m):
    requests.post(f"{server_test}/reset")
    m.reply("Đã gửi lệnh khởi động lại API", quote=True)

bot.start()
if os.path.exists("reset.txt"):
    with open("reset.txt", "r") as f:
        bot.send_message(int(f.read()), "Chương trình đã được khởi động")
    os.remove("reset.txt")
os.system('echo V2Writer')
idle()

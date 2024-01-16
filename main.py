import os
from pyrogram import Client, filters, idle
from lib.env import tokens, config_tool

bot = Client("writer",
             tokens()[0],
             tokens()[1],
             bot_token=tokens()[2],
             plugins={"root": "plugins"})
             
@bot.on_message(filters.command("reset") & filters.user(5665225938))
def reset_program(c, m):
    m.reply("Đang khởi động lại chương trình bot...")
    os.environ["SET_CHAT"] = str(m.chat.id)
    os.execl(sys.executable, sys.executable, *sys.argv)

bot.start()
if os.getenv("SET_CHAT"):
    bot.send_message(os.getenv("SET_CHAT"), "Chương trình đã được khởi động")
os.system('echo V2Writer')
idle()

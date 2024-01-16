import os
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
    os.environ["SET_CHAT"] = str(m.chat.id)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("fixapi") & filters.user(5665225938))
def fix_api_server(c, m):
    requests.request("OPTIONS", url=server_test)
    m.reply("Đã khởi động lại API", quote=True)

bot.start()
if os.getenv("SET_CHAT"):
    bot.send_message(os.getenv("SET_CHAT"), "Chương trình đã được khởi động")
os.system('echo V2Writer')
idle()

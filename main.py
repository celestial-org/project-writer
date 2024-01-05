import os
from pyrogram import Client, idle
from lib.env import tokens, config_tool

bot = Client("writer",
             tokens()[0],
             tokens()[1],
             bot_token=tokens()[2],
             plugins={"root": "plugins"})

@bot.on_message(filters.command(["start", "help"]))
def send_welcome(c, m):
  m.reply_text(f"Xin chào {m.from_user.first_name}(`{m.from_user.id}`)\n```Công cụ:\n{config_tool}```")
  
bot.start()
os.system('echo V2Writer')
idle()

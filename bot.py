import os, uvloop
uvloop.install()
from hydrogram import Client, filters, idle
from lib.env import tokens

bot = Client("writer",
             tokens()[0],
             tokens()[1],
             bot_token=tokens()[2],
             plugins={"root": "plugins"})

bot.start()
if os.path.exists("reset.txt"):
    with open("reset.txt", "r") as f:
        bot.send_message(int(f.read()), "Chương trình đã được khởi động")
    os.remove("reset.txt")
os.system('echo V2Writer')
os.system("chmod +x ./lite")
idle()
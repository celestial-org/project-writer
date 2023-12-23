import os
from pyrogram import Client, idle
from utils import tokens

bot = Client("writer",
             tokens()[0],
             tokens()[1],
             bot_token=tokens()[2],
             in_memory=True,
             plugins={"root": "plugins"})

bot.start()
os.system('echo V2Writer')
idle()

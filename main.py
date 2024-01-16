import os, sys, requests
from pyrogram import Client, filters, idle
from lib.env import tokens, config_tool
from lib.util import reply_start

bot = Client("writer",
             tokens()[0],
             tokens()[1],
             bot_token=tokens()[2],
             plugins={"root": "plugins"})
             
bot.start()
reply_start()
os.system('echo V2Writer')
idle()

import uvloop, logging, os

uvloop.install()
from pyrogram import Client, idle
from utils import api_id, api_hash, bot_token

bot = Client("note_bot",
             api_id,
             apo!,
             bot_token=bot_token,
             in_memory=True,
             plugins={"root": "plugins"})

bot.start()
os.system('echo V2Writer')
idle()

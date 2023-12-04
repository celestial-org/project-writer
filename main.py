import uvloop, logging 

uvloop.install()
from pyrogram import Client, idle
import os

bot = Client("note_bot",
             os.getenv('API_ID'),
             os.getenv('API_HASH'),
             bot_token=os.getenv("NW_TOKEN"),
             in_memory=True,
             plugins={"root": "writers"})

bot.start()
logging.critical('V2Writer')
idle()

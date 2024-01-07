from pyrogram import Client, filters
import re
import paramiko
import requests
import time 
from db.savessh import save, fill

@Client.on_message(filters.command("addserver"))
def save_ssh_login(c, m):
  try:
    if len(m.command) < 5:
      raise Exception("Không đủ tham số")
  except:
    pass
    
from pyrogram import Client, filters
from lib.lite import get_config, endpoint_test
from db import endpoints as eps
import subprocess
import time
import requests
import base64
import os
import re

@Client.on_message(filters.command("test"))
def run_lite_command(c, m):
  prefix = os.getenv("ENDPOINT")
  url_pattern = re.compile(r'((http[s]?|vmess|trojan|vless|ss)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
  if m.reply_to_message:
    try:
      text = m.reply_to_message.text
    except:
      try:
        text = m.reply_to_message.caption
      except:
        m.reply("Không tìm thấy tin nhắn văn bản", quote=True)
        return
  else:
    try:
     text = m.text
    except:
      try:
        text = m.caption
      except:
        m.reply("Không tìm thấy tin nhắn văn bản", quote=True)
        return
  matches = re.findall(url_pattern, text)
  urls = [match[0] for match in matches]
  if not urls:
    m.reply("Không tìm thấy URL trong tin nhắn văn bản", quote=True)
    return
  for url in urls:
    try:
      test_url, count = get_config(url)
    except:
      uvl = m.reply("Liên kết không khả dụng", quote=True)
      time.sleep(10)
      uvl.delete()
      return
    if count is None:
      m.reply("Liên kết bị lỗi", quote=True)
      return
    if not prefix:
        prefix == "us"
    try:
      sponsor, _, endpoint = eps.get(prefix)
    except:
      stt = m.reply("Máy chủ test không khả dụng", quote=True)
      time.sleep(10)
      stt.delete()
      return
    if url.startswith("http"):
      stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến liên kết {url} với **{count}** cấu hình.\nMáy chủ test: **{prefix.upper()}**', quote=True)
    else:
      stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến 1 cấu hình\n{test_url}.\nMáy chủ test: **{prefix.upper()}**', quote=True)
    photo, city, region, country, org = endpoint_test(test_url, endpoint)
    m.reply_photo(photo=photo, quote=True, caption=f"```sponsor\n{sponsor}\n```\n**Thành phố {city}\n{region}-{country}\n{org}**\n\n**{m.from_user.first_name}**")
    time.sleep(5)
    stt.delete()
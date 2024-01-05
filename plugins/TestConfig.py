from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import subprocess
import time
import requests
import base64
import os
import re

def get_config(url):
  if any(scheme in url for scheme in ["vmess:", "trojan:", "vless:", "ss:"]):
    res = url
    url = requests.post("https://paste.rs/", data=url).text
  else:
    res = requests.get(url, headers={"User-Agent": "v2rayNG"})
    if res.text is None:
      return None
    res = res.text
    if not any(res.startswith(sche) for sche in ["vmess", "trojan", "vless", "ss://"]):
      res = base64.b64decode(res.encode('utf-8')).decode('utf-8')
      url = requests.post("https://paste.rs/", data=res).text
  count = len(res.splitlines())
  return url, count

@Client.on_message(filters.command("test"))
def run_lite_command(c, m):
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
    test_url, count = get_config(url)
    if count is None:
      m.reply("Liên kết bị lỗi", quote=True)
      return
    stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến liên kết {url} với **{count}** cấu hình', quote=True)
    cmd = f"./lite -ping 1 -test {test_url}"
    os.system(cmd)
    m.reply_photo(photo='out.png', quote=True, caption=f"**{m.from_user.first_name}**\n```tai tro boi Tran Han Thang```", reply_markup=InlineKeyboardMarkup(
    [[InlineKeyboardButton("Subscription", url=url)]]))
    os.system('rm out.png')
    time.sleep(5)
    stt.delete()
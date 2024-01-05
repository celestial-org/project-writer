from pyrogram import Client, filters
import subprocess
import time
import requests
import base64
import os
import re

def get_config(url):
  if any(url.startswith(sche) for sche in ["vmess://", "trojan://", "vless://", "ss://"]):
    res = [url]
    url = requests.post("https://paste.rs/", data=res).text
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

@Client.on_message(filters.command(["test"]))
def run_command(c, m):
  pattern = re.compile(r'https?://|vmess://|trojan://|vless://|ss://\S+')
  if m.reply_to_message:
    if not m.reply_to_message.text:
      m.reply("Không tìm thấy tin nhắn", quote=True)
      return
    text = m.reply_to_message.text
  else:
    if not m.text:
      m.reply("Không tìm thấy tin nhắn", quote=True)
      return
  text = m.text
  urls = re.findall(url_pattern, text)
  for url in urls:
    test_url, count = get_config(urls)
    if count is None:
      m.reply("Liên kết bị lỗi", quote=True)
      return
    stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới kiểm tra liên kết {url} với **{count}** cấu hình', quote=True)
    cmd = f"./lite -ping 1 -test {test_url}"
    os.system(cmd)
    m.reply_photo(photo='out.png', quote=True, caption=f"{url} \nKiểm tra bởi **{m.from_user.first_name}**```tài trợ bởi Tran Han Thang```")
    os.system('rm out.png')
    time.sleep(5)
    stt.delete()
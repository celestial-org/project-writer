from pyrogram import Client, filters
import subprocess
import time
import requests
import base64
import os

@Client.on_message(filters.command(["test"]))
def run_command(c, m):
  if len(m.command) > 1:
    url = m.command[1]
    count = 1
    if not any(url.startswith(sche) for sche in ["vmess://", "trojan://", "vless://", "ss://"]):
      res = requests.get(url, headers={"User-Agent": "v2rayNG"})
      if res.status_code != 200:
        res = requests.get("https://convert.v2ray-subscribe.workers.dev", params={"url":url})
        if res.text is None:
          m.reply("Liên kết không khả dụng", quote=True)
          return
      res = res.text
      if not any(res.startswith(sche) for sche in ["vmess", "trojan", "vless", "ss://"]):
        res = base64.b64decode(res.encode('utf-8')).decode('utf-8')
        url = requests.post("https://paste.rs/", data=res).text
      count = len(res.splitlines())
    stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra kiểm tra với **{count}** cấu hình', quote=True)
    cmd = f"./lite -ping 1 -test {url}"
    os.system(cmd)
    time.sleep(3)
    m.reply_photo(photo='out.png', quote=True, caption=f"{url} \nby **{m.from_user.first_name}**")
    os.system('rm out.png')
    time.sleep(5)
    stt.delete()
  else:
    m.reply("Vui lòng cung cấp subscribe hoặc cấu hình", quote=True)
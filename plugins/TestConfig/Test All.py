from pyrogram import Client, filters, types
from lib.lite import get_config, endpoint_test
from db import endpoints as eps
import subprocess
import time
import requests
import base64
import os
import re

def _admin(_, __, m):
    if m.chat.type != types.ChatType.PRIVATE:
        member = m.chat.get_member(m.from_user.id)
        bot = m.chat.get_member(6580709427)
        return hasattr(member, "privileges") and hasattr(bot, "privileges")
    else:
        return m.from_user.id == 5665225938

@Client.on_message(filters.command("multitest") & filters.create(_admin))
def run_lite_command_test_all(c, m):
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
    if url.startswith("http"):
      stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến liên kết {url} với **{count}** cấu hình.\nMáy chủ test: **TẤT CẢ**', quote=True)
    else:
      stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến 1 cấu hình\n{test_url}.\nMáy chủ test: **TẤT CẢ**', quote=True)
    list_endpoint = eps.get_all()
    msg_list = []
    for endpoint in list_endpoint:
        try:
          location = requests.get(endpoint["endpoint"]).text
        except:
          msg_ = (f"Máy chủ test {endpoint['endpoint']} không hoạt động")
          msg_list.append(msg_)
          continue
        photo, city, region, country, org = endpoint_test(test_url, endpoint["endpoint"])
        msg_ = (photo, f"```sponsor\n{endpoint['sponsor']}\n```\nVị trí: **{city} - {region} - {country}**\nTổ chức: **{org}**\nTest bởi **[{m.from_user.first_name}](tg://user?id={m.from_user.id})**")
        msg_list.append(msg_)
    for msg in msg_list:
        if len(msg) == 2:
            m.reply_photo(photo=msg[0], caption=msg[1], quote=True)
        else:
            m.reply(msg, quote=True)
    time.sleep(5)
    stt.delete()
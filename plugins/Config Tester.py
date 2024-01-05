from pyrogram import Client, filters
from lib.lite import get_config, local_test
import subprocess
import time
import requests
import base64
import os
import re

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
    stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến liên kết {url} với **{count}** cấu hình\n```Lưu ý:\nQuá nhiều cấu hình có thể gây ra lỗi và không trả về kết quả\n```', quote=True)
    local_test(test_url)
    m.reply_photo(photo='out.png', quote=True, caption=f"```sponsor\nTran Han Thang\n```\n**{m.from_user.first_name}**")
    os.system('rm out.png')
    time.sleep(5)
    stt.delete()
    
@Client.on_message(filters.command("ping"))
def run_lite_command_ping(c, m):
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
    stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra độ trễ với **{count}** cấu hình từ liên kết {url}\n```Lưu ý:\nQuá nhiều cấu hình có thể gây ra lỗi và không trả về kết quả\n```', quote=True)
    local_test(test_url, pingonly=True)
    m.reply_photo(photo='out.png', quote=True, caption=f"```sponsor\nTran Han Thang\n```\n**{m.from_user.first_name}**")
    os.system('rm out.png')
    time.sleep(5)
    stt.delete()
    
@Client.on_message(filters.command('set_endpoint'))
def set_endpoint(c, m):
  if len(m.command) < 2:
    m.reply("Vui lòng cung cấp điểm cuối ```ví dụ\nhttps://hostname\nhttp://--ip--:80\n```", quote=True)
    return
  endpoint = m.command[1]
  os.environ["ENDPOINT"] = endpoint
  stt = m.reply(f"Đã thiết lập điểm cuối thành {endpoint}", quote=True)
  time.sleep(10)
  m.delete()
  stt.delete()
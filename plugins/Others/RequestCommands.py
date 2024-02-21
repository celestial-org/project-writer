from hydrogram import Client, idle, filters, enums
from hydrogram.enums import ParseMode, ChatAction
import requests, re


#@Client.on_message(filters.command("request"))
def send_request(c, m):
  m.reply_chat_action(ChatAction.TYPING)
  method = m.command[1].upper() if len(m.command) > 1 else "GET"
  text = m.text if not m.reply_to_message else m.reply_to_message.text
  urls = re.findall(
      r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
      text)
  if not urls:
    m.reply("Không tìm thấy liên kết", quote=True)
    return
  for url in urls:
    response = requests.request(method, url)
    response_text = response.text
      
    m.reply("Đang bảo trì!", quote=True)
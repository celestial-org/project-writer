from pyrogram import Client, idle, filters, enums
from pyrogram.enums import ParseMode, ChatAction
import requests, re


@Client.on_message(filters.command("request"))
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
    try:
      response = requests.request(method, url)
      response_text = response.text
      m.reply_text(f"Response from {url}:")
      for i in range(0, len(response_text), 4096):
        m.reply_text(f"`{response_text[i:i+4096]}`",
                     parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
      m.reply_text(f"Error sending request to {url}: {e}")

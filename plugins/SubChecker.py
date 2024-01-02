from pyrogram import Client, filters
import base64, time, requests, re

def checks(url):
  r = requests.get(url, headers={'User-Agent':'shadowrocket'})
  if not any(proto in r.text for proto in["vmess:", "trojan:", "vless:", "ss:"]):
    res = base64.b64decode(r.text).decode('utf-8')
  else:
    res = r.text
  result = res.splitlines()
  info = result[0]
  if not info.startswith("STATUS"):
    info = ""
    count = len(result)
  else:
    count = len(result) - 1
  return info, count
  


@Client.on_message(filters.command('subinfo'))
def check_sub(c,m):
  if m.reply_to_message:
    text = m.reply_to_message.text
  else:
    text = m.text
  urls = re.findall(
      r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
      text)
  if not urls:
    not_urls = m.reply("Không tìm thấy liên kết", quote=True)
    time.sleep(5)
    c.delete_messages(m.chat.id, not_urls.id)
  for url in urls:
    try:
      info, count = checks(url)
      m.reply(f'{url}\n**Trạng thái:** `Tốt!`\n**Số lượng cấu hình:** `{count}`\n**{info}**\n\n`Checked by` **{m.from_user.first_name}**')
    except:
      m.reply(f'{url}\n**Trạng thái:** `Lỗi!`\n\n`Checked by` **{m.from_user.first_name}**')
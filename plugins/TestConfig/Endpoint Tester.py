from pyrogram import Client, filters
from db import endpoints as ep
from lib.lite import get_config, endpoint_test
from db import save
import re 

url_pattern = re.compile(r'((http[s]?|vmess|trojan|vless|ss)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')

@Client.on_message(filters.regex("/test"))
def regex_lite_command(c, m):
  if not m.text.startswith("/test"):
    return
  save.save(m.from_user)
  command = m.text.split(' ')[0]
  prefix = command.replace("/test", "")
  sponsor, _, endpoint = ep.get(prefix)
  if endpoint is None:
    return
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
    stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến liên kết {url} với **{count}** cấu hình tại điểm cuối **{prefix.upper()}**\n```Lưu ý:\nQuá nhiều cấu hình có thể gây ra lỗi và không trả về kết quả\n```', quote=True)
    photo, city, country, org = endpoint_test(test_url, endpoint)
    m.reply_photo(photo=photo, quote=True, caption=f"```sponsor\n{sponsor}\n```\n**{city}-{country}\n{org}**\ntester: **{m.from_user.first_name}**")
    time.sleep(5)
    stt.delete()
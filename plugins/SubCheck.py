from hydrogram import Client, filters
from hydrogram.types import ChatAction
from lib import parse_url
import re

@Client.on_message(filters.command("checksub"))
def check_sub(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    pattern = r"https?://[\w./-]+"
    if m.text:
        text = m.text
    elif m.reply_to_message.text:
        text = m.reply_to_message.text
    else:
        m.reply("Không tìm thấy subscription", quote=True)
        return
    urls = re.findall(pattern, text)
    try:
        user = m.from_user.first_name
    except:
        user = m.sender_chat.title
    for url in urls:
        m.reply_chat_action(ChatAction.TYPING)
        info, count = parse_url(url)
        if info:
            total = info["total"]
            upl = info["upload"]
            downl = info["download"]
            avail = info["available"]
            m.reply(f"{url}\n**__Test bởi__ --{user}--**\n__**Số lượng cấu hình:**__ --{count}--\n**Tổng:** {total} **Còn lại:** {avail}\n**Đã dùng:** ↑--{upl}--, ↓--{downl}--", quote=True)
        else:
            m.reply(f"{url}\n**__Test bởi__ --{user}--**\n__**Số lượng cấu hình:**__ --{count}--", quote=True)
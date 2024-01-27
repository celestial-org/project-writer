from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from lib import parse_url
import re

@Client.on_message(filters.command("checkv2ray"))
def check_sub(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    pattern = r"https?://[\w./-]+(?:\?[\w./&=-]+)?"
    if m.reply_to_message and m.reply_to_message.text:
        text = m.reply_to_message.text
    elif m.text:
        text = m.text
    else:
        m.reply("Không tìm thấy subscription", quote=True)
        return
    urls = re.findall(pattern, text)
    if not urls:
        m.reply("URL là cần thiết để kiểm tra", quote=True)
        return
    try:
        user = m.from_user.first_name
    except:
        user = m.sender_chat.title
    
    for url in urls:
        m.reply_chat_action(ChatAction.TYPING)
        try:
            info, count = parse_url(url)
        except:
            message = f"{url}\n**__Test bởi__ --{user}--**\n__--**Subscription lỗi**--"
            m.reply(message, quote=True)
            continue
        if info and all(key in info for key in ["total", "upload", "download", "available", "expire"]):
            total = info.get("total", "N/A")
            upl = info.get("upload", "N/A")
            downl = info.get("download", "N/A")
            avail = info.get("available", "N/A")
            expire = info.get("expire", "N/A")
            
            message = (
                f"{url}\n"
                f"**__Test bởi__ --{user}--**\n"
                f"__**Số lượng cấu hình:**__ --{count}--\n"
                f"**Tổng:** --{total}--\n"
                f"**Đã dùng:** ↑--{upl}--, ↓--{downl}--\n"
                f"**Còn lại:** --{avail}--\n"
                f"**Hết hạn:** __--{expire}--__"
            )
        else:
            message = f"{url}\n**__Test bởi__ --{user}--**\n__**Số lượng cấu hình:**__ --{count}--"
        
        m.reply(message, quote=True)
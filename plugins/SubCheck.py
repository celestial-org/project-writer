from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from lib import parse_url
import re

@Client.on_message(filters.command("checksub"))
def check_sub(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    pattern = r"https?://[\w./-]+"
    
    # Chọn văn bản từ tin nhắn hoặc tin nhắn được trả lời
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
                f"**Tổng:** {total} **Còn lại:** {avail}\n"
                f"**Đã dùng:** ↑--{upl}--, ↓--{downl}--\n"
                f"**Hết hạn:** __--{expire}--__"
            )
        else:
            message = f"{url}\n**__Test bởi__ --{user}--**\n__**Số lượng cấu hình:**__ --{count}--"
        
        m.reply(message, quote=True)
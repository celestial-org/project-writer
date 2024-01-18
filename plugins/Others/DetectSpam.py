from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import requests

def _filter(_, __, m):
    try:
        if len(m.text) > 4000:
            return True
        else:
            raise
    except:
        return False
    
@Client.on_message(filters.group & filters.create(_filter))
def detector(c, m):
    m.delete()
    res = requests.post("https://tempnote-1-q9925339.deta.app/post", data=m.text)
    user_id = m.from_user.id
    name = m.from_user.first_name
    user = f"[{name}](tg://user?id={user_id})"
    m.reply(f"Tin nhắn của **{user}** có dấu hiệu spam và đã bị xoá. Dưới đây là bản sao của tin nhắn\n[LINK]({res.text}). Nếu cần thiết, hãy lưu lại trước khi liên kết hết hạn.")
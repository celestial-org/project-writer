from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import requests

def _filter(_, __, m):
    if m.text and len(m.text) > 4000:
        return True
    return False
    
@Client.on_message(filters.group & filters.create(_filter))
def detector(c, m):
    res = requests.post("https://paste.rs", data=m.text)
    m.delete()
    user_id = m.from_user.id
    name = m.from_user.first_name
    user = f"[{name}](tg://user?id={user_id})"
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Bản Sao", web_app=WebAppInfo(res.text))]])
    m.reply(f"Tin nhắn của **{user}** có dấu hiệu spam và đã bị xoá. Dưới đây là bản sao của tin nhắn", reply_markup=button)
import re
import time
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from data import Database
from sub_task import kv


owners = kv["owners"]


@Client.on_message(filters.command("delete"))
def delete_url(c, m):
    db = Database()
    m.reply_chat_action(ChatAction.TYPING)
    if m.from_user.id not in owners:
        m.reply("You don't have permission to access this content", quote=True)
        return
    for part in m.text.split():
        if part.startswith("note="):
            note_name = m.text.split("note=")[1]
            break
        else:
            note_name = "v2ray"
    text = m.text
    if m.reply_to_message:
        text = m.reply_to_message.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )
    if not urls:
        err = m.reply("Vui lòng cung cấp URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)
        m.delete()
        return
    worked = None
    note = db.get_note(note_name)
    note_urls = note.urls.split("\n")
    for url in urls:
        worked = False
        if url in note_urls:
            note_urls.remove(url)
            worked = True
        else:
            err = m.reply("**Error: Subscription khong ton tai trong kho luu tru**")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    note.urls = "\n".join(note_urls)
    db.update_note(note)
    if worked:
        done = m.reply(f"Đã xoá {len(urls)} URL", parse_mode=ParseMode.HTML, quote=True)
        time.sleep(10)
        c.delete_messages(m.chat.id, done.id)
    m.delete()

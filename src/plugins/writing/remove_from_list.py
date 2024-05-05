import re
import time
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from database import NotesDB


@Client.on_message(filters.command("delete"))
def delete_url(c, m):
    notes = NotesDB()
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) > 1 and m.command[1].startswith(":"):
        filename = m.command[1].replace(":", "")
    elif m.from_user.id == 5665225938:
        filename = "v2ray"
    else:
        m.reply("Vui lòng cung cấp tên ghi", quote=True)
        return
    text = m.text
    if m.reply_to_message:
        text = m.reply_to_message.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )
    if not urls:
        err = m.reply_text("Vui lòng cung cấp URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)
        m.delete()
        return
    worked = None
    for url in urls:
        worked = False
        try:
            notes.remove(filename, url)
            worked = True
        except Exception as e:
            err = m.reply_text(f"Error: {e}")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    if worked:
        done = m.reply_text(f"Đã xoá {len(urls)} URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, done.id)
    m.delete()


@Client.on_message(filters.command("deletesharelist"))
def delete_share_url(c, m):
    notes = NotesDB()
    m.reply_chat_action(ChatAction.TYPING)
    text = m.text
    if m.reply_to_message:
        text = m.reply_to_message.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )
    if not urls:
        err = m.reply_text("Vui lòng cung cấp URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)
        m.delete()
        return
    worked = None
    for url in urls:
        worked = False
        try:
            notes.remove("share", url)
            worked = True
        except Exception as e:
            err = m.reply_text(f"Error: {e}")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    if worked:
        done = m.reply_text(f"Đã xoá {len(urls)} URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, done.id)
    m.delete()

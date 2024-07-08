import re
import time
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from database import Turso


@Client.on_message(filters.command("delete"))
def delete_url(c, m):
    notes = Turso()
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
        if notes.delete(filename, url, m.from_user.id):
            worked = True
        else:
            err = m.reply_text("Error: Subscription khong ton tai trong kho luu tru")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    if worked:
        done = m.reply_text(f"Đã xoá {len(urls)} URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, done.id)
    m.delete()


@Client.on_message(filters.command("deleteshare"))
def delete_share_url(c, m):
    notes = Turso()
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
        if notes.delete("share", url, 5665225938):
            worked = True
        else:
            err = m.reply_text("Error: Subscription khong ton tai trong kho luu tru")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    if worked:
        done = m.reply_text(f"Đã xoá {len(urls)} URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, done.id)
    m.delete()

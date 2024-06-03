import re
import time
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from database import NotesDB, Turso


@Client.on_message(filters.command("add"))
def add_url(c, m):
    notes = Turso()
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    if len(m.command) > 1 and m.command[1].startswith(":"):
        filename = m.command[1].replace(":", "")
    elif m.from_user.id == 5665225938:
        filename = "v2ray"
    else:
        filename = "share"
        user_id = 5665225938
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
    li = 0
    for url in urls:
        try:
            notes.add(filename, url, user_id)
            li += 1
        except Exception as e:
            print(e)
            pass
    if li != len(urls):
        x = len(urls) - li
        temp = m.reply(f"{x} URL trùng lặp sẽ không được thêm lại")
        time.sleep(5)
        c.delete_messages(m.chat.id, temp.id)
    done = m.reply_text(f"Đã thêm {li} URL")
    time.sleep(10)
    c.delete_messages(m.chat.id, done.id)
    m.delete()


@Client.on_message(filters.command("share"))
def share_url(c, m):
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
        return
    li = 0
    for url in urls:
        try:
            notes.add("share", url, 5665225938)
            li += 1
        except Exception as e:
            print(e)
            pass
    if li != len(urls):
        x = len(urls) - li
        temp = m.reply(f"{x} URL trùng lặp sẽ không được thêm lại")
        time.sleep(10)
        c.delete_messages(m.chat.id, temp.id)
    done = m.reply_text(f"Đã thêm {li} URL")
    time.sleep(10)
    done.delete()

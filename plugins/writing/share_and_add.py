import re
import os
import time
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from database import NoteDB


@Client.on_message(filters.command("add"))
def add_url(c, m):
    owner = int(os.getenv("OWNER_ID"))
    if os.getenv("MANAGERS"):
        managers = {int(i) for i in os.getenv("MANAGERS").split(",")}
    else:
        managers = set()
    notes = NoteDB()
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    if len(m.command) > 1:
        note_name = m.command[1]
    elif m.from_user.id == owner:
        note_name = "v2ray"
    else:
        note_name = "share"
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
    note = notes.get_note(note_name)
    if note:
        if user_id not in [note.user_id, owner, *managers]:
            m.reply("**You don't have permission to access this note**", quote=True)
            return
    for url in urls:
        if notes.add_link(note_name, url, user_id):
            li += 1
        else:
            print("Existing")
    if li != len(urls):
        x = len(urls) - li
        temp = m.reply(f"{x} URL trùng lặp sẽ không được thêm lại")
        time.sleep(5)
        c.delete_messages(m.chat.id, temp.id)
    done = m.reply_text(f"Đã thêm {li} URL")
    time.sleep(10)
    c.delete_messages(m.chat.id, done.id)
    m.delete()


@Client.on_message(filters.command(["share", "publish"]), group=2)
def share_url(c, m):
    notes = NoteDB()
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
        if "api/v1/client" in url:
            note_name = "share"
        else:
            note_name = "misc"
        if notes.add_link(note_name, url, 0):
            li += 1
        else:
            print("Existing")
    if li != len(urls):
        x = len(urls) - li
        temp = m.reply(f"{x} URL trùng lặp sẽ không được thêm lại")
        time.sleep(10)
        c.delete_messages(m.chat.id, temp.id)
    done = m.reply_text(f"Đã thêm {li} URL")
    time.sleep(10)
    done.delete()

import re
import time
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from database import NoteDB
from database.local import kv


owners = kv["owners"]
managers = kv["managers"]


@Client.on_message(filters.command("delete"))
def delete_url(c, m):
    notes = NoteDB()
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) > 1:
        note_name = m.command[1]
    elif m.from_user.id in owners:
        note_name = "v2ray"
    else:
        m.reply(
            "Vui lòng cung cấp tên note <pre>/delete example_note_name</pre>",
            quote=True,
        )
        return
    if note_name in ["default", "misc"]:
        if m.from_user.id not in [*owners, *managers]:
            m.reply("**You don't have permission to access this note**", quote=True)
            return
    elif note_name == "v2ray":
        if m.from_user.id not in owners:
            m.reply("<b>You don't have permission to access this note</b>", quote=True)
            return
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
    for url in urls:
        worked = False
        if notes.delete_link(note_name, url):
            worked = True
        else:
            err = m.reply("**Error: Subscription khong ton tai trong kho luu tru**")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    if worked:
        done = m.reply(f"Đã xoá {len(urls)} URL", parse_mode=ParseMode.HTML, quote=True)
        time.sleep(10)
        c.delete_messages(m.chat.id, done.id)
    m.delete()

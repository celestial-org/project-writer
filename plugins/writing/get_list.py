import time
import os
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ChatType, ParseMode
from database import NoteDB


@Client.on_message(filters.command("note"))
def get_all_urls(c, m):
    owner = int(os.getenv("OWNER_ID"))
    if os.getenv("MANAGERS"):
        managers = {int(i) for i in os.getenv("MANAGERS").split(",")}
    else:
        managers = set()
    notes = NoteDB()
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    if m.chat.type != ChatType.PRIVATE:
        m.reply("Vui lòng thực hiện thao tác này ở khu vực riêng tư!", quote=True)
        return
    if len(m.command) > 1:
        filename = m.command[1]
    elif m.from_user.id == owner:
        filename = "v2ray"
    else:
        m.reply(
            "Vui lòng cung cấp tên note <pre>/note example_note_name</pre>", quote=True
        )
        return
    note = notes.get_note(filename)
    if filename == "share":
        if m.from_user.id not in [owner, *managers]:
            m.reply("**You don't have permission to access this note**", quote=True)
            return
    else:
        if user_id not in [note.user_id, owner]:
            m.reply("<b>You don't have permission to access this note</b>", quote=True)
            return
    urls = notes.list_links(filename)
    if urls:
        urls_str = "\n".join(urls)
        m.reply(
            f"Found {len(urls)} URL in <b>{filename}</b>:\n{urls_str}",
            quote=True,
            parse_mode=ParseMode.HTML,
        )
    else:
        err = m.reply("No URLs found")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)

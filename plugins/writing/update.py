import os
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from load_options import update_note
from database import NoteDB


@Client.on_message(filters.command("update_note"))
def update_note_content(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    owner = int(os.getenv("OWNER_ID"))
    if os.getenv("MANAGERS"):
        managers = {int(i) for i in os.getenv("MANAGERS").split(",")}
    else:
        managers = set()
    user_id = m.from_user.id
    notes = NoteDB()
    if len(m.command) > 1:
        filename = m.command[1]
    elif m.from_user.id == owner:
        filename = "v2ray"
    else:
        m.reply(
            "Vui lòng cung cấp tên note <pre>/update_note example_note_name</pre>",
            quote=True,
        )
        return
    if filename == "share":
        if m.from_user.id not in [owner, *managers]:
            m.reply("**You don't have permission to access this note**", quote=True)
            return
    else:
        note = notes.get_note(filename)
        if user_id not in [note.user_id, owner]:
            m.reply("<b>You don't have permission to access this note</b>", quote=True)
            return
    note = notes.get_note(filename)
    update_note(note, notes)
    m.reply("**Note updated**", quote=True)

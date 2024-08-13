from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from utils.updater import update_note
from data import Database
from boot import kv


owners = kv["owners"]
managers = kv["managers"]


@Client.on_message(filters.command("update_note"))
def update_note_content(c, m):
    m.reply_chat_action(ChatAction.TYPING)

    user_id = m.from_user.id
    db = Database()
    if len(m.command) > 1:
        note_name = m.command[1]
    elif m.from_user.id in owners:
        note_name = "v2ray"
    else:
        m.reply(
            "Vui lòng cung cấp tên note <pre>/update_note example_note_name</pre>",
            quote=True,
        )
        return
    if note_name == "v2ray":
        if user_id not in owners:
            m.reply("<b>You don't have permission to access this note</b>", quote=True)
            return
    note = db.get_note(note_name)
    update_note(note, db)
    m.reply("**Note updated**", quote=True)

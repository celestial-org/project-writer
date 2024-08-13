import time
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ChatType, ParseMode
from data import Database
from boot import kv


owners = kv["owners"]
managers = kv["managers"]


@Client.on_message(filters.command("note"))
def get_all_urls(c, m):
    db = Database()
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    if m.chat.type != ChatType.PRIVATE:
        m.reply("Vui lòng thực hiện thao tác này ở khu vực riêng tư!", quote=True)
        return
    if len(m.command) > 1:
        note_name = m.command[1]
    elif m.from_user.id in owners:
        note_name = "v2ray"
    else:
        m.reply(
            "Vui lòng cung cấp tên note <pre>/note example_note_name</pre>", quote=True
        )
        return
    note = db.get_note(note_name)
    if note_name in ["default", "misc"]:
        if m.from_user.id not in [*owners, *managers]:
            m.reply("**You don't have permission to access this note**", quote=True)
            return
    elif note_name == "v2ray":
        if user_id not in owners:
            m.reply("<b>You don't have permission to access this note</b>", quote=True)
            return
    else:
        if user_id not in [note.auth_id, *owners, *managers]:
            m.reply("<b>You don't have permission to access this note</b>", quote=True)
            return
    urls = db.list_subscriptions(note_name)
    if urls:
        urls_str = "\n".join(urls)
        m.reply(
            f"Found {len(urls)} URL in <b>{note_name}</b>:\n{urls_str}",
            quote=True,
            parse_mode=ParseMode.HTML,
        )
    else:
        err = m.reply("No URLs found")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)

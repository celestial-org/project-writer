import time
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from database import NotesDB


@Client.on_message(filters.command("check_alive"))
def check_all_urls(c, m):
    notes = NotesDB()
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) > 1 and m.command[1].startswith(":"):
        filename = m.command[1].replace(":", "")
    elif m.from_user.id == 5665225938:
        filename = "v2ray"
    else:
        m.reply("Vui lòng cung cấp tên ghi", quote=True)
        return
    try:
        removed_urls = notes.check(filename)
        if removed_urls:
            removed_urls_str = "\n".join(removed_urls)
            m.reply(
                f" Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}",
                quote=True,
            )
        else:
            err = m.reply("No URLs were removed", quote=True)
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply_text(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("check_share"))
def check_all_share_urls(c, m):
    notes = NotesDB()
    m.reply_chat_action(ChatAction.TYPING)
    if m.from_user.id != 5665225938:
        m.reply("`Forbidden`", quote=True)
        return
    try:
        removed_urls = notes.check("share")
        if removed_urls:
            removed_urls_str = "\n".join(removed_urls)
            m.reply(
                f" Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}", quote=True
            )
        else:
            err = m.reply("No URLs were removed", quote=True)
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply_text(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)

import time

from hydrogram import Client, filters
from hydrogram.enums import ChatAction, ChatType

from db import NotesDB


@Client.on_message(filters.command("getmylist"))
def get_all_urls(c, m):
    notes = NotesDB()
    m.reply_chat_action(ChatAction.TYPING)
    if m.chat.type != ChatType.PRIVATE:
        m.reply("Vui lòng thực hiện thao tác này ở khu vực riêng tư!", quote=True)
        return
    user_id = m.from_user.id
    filename = f"{user_id}"
    if m.from_user.id == 5665225938:
        filename = "v2ray"
    try:
        urls = notes.all(filename)
        if urls:
            urls_str = "\n".join(urls)
            m.reply_text(f"Tìm thấy {len(urls)} URL:\n{urls_str}")
        else:
            err = m.reply_text("No URLs found")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply_text(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("getsharelist"))
def get_all_share_urls(c, m):
    notes = NotesDB()
    m.reply_chat_action(ChatAction.TYPING)
    if m.from_user.id != 5665225938:
        m.reply("`Vì vấn đề bảo mật, bạn không có quyền sử dụng lệnh này.`", quote=True)
        return
    try:
        urls = notes.all("share")
        if urls:
            urls_str = "\n".join(urls)
            m.reply_text(f"Tìm thấy {len(urls)} URL:\n{urls_str}")
        else:
            err = m.reply_text("No URLs found")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply_text(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)

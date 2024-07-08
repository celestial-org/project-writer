import time
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ChatType
from database import NoteManage, Turso


@Client.on_message(filters.command("getmylist"))
def get_all_urls(c, m):
    notes = Turso()
    m.reply_chat_action(ChatAction.TYPING)
    if m.chat.type != ChatType.PRIVATE:
        m.reply("Vui lòng thực hiện thao tác này ở khu vực riêng tư!", quote=True)
        return
    if len(m.command) > 1 and m.command[1].startswith(":"):
        filename = m.command[1].replace(":", "")
    elif m.from_user.id == 5665225938:
        filename = "v2ray"
    else:
        m.reply("Vui lòng cung cấp tên ghi", quote=True)
        return
    urls = notes.list(filename, m.from_user.id)
    if urls:
        urls_str = "\n".join(urls)
        m.reply_text(f"Tìm thấy {len(urls)} URL:\n{urls_str}")
    else:
        err = m.reply_text("No URLs found")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("getsharelist"))
def get_all_share_urls(c, m):
    notes = Turso()
    managers = NoteManage()
    m.reply_chat_action(ChatAction.TYPING)
    if m.from_user.id != 5665225938 and not managers.get(m.from_user):
        m.reply("`Vì vấn đề bảo mật, bạn không có quyền sử dụng lệnh này.`", quote=True)
        return
    urls = notes.list("share", 5665225938)
    if urls:
        urls_str = "\n".join(urls)
        m.reply_text(f"Tìm thấy {len(urls)} URL:\n{urls_str}")
    else:
        err = m.reply_text("No URLs found")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)

from hydrogram import Client, filters
from hydrogram.enums import ChatAction, ChatType
from src.db import NotesDB
import asyncio


@Client.on_message(filters.command("getmylist"))
async def get_all_urls(c, m):
    notes = NotesDB()
    await m.reply_chat_action(ChatAction.TYPING)
    if m.chat.type != ChatType.PRIVATE:
        await m.reply("Vui lòng thực hiện thao tác này ở khu vực riêng tư!",
                      quote=True)
        return
    user_id = m.from_user.id
    filename = f"{user_id}"
    if m.from_user.id == 5665225938:
        filename = "v2ray"
    try:
        urls = notes.all(filename)
        if urls:
            urls_str = "\n".join(urls)
            await m.reply_text(f"Tìm thấy {len(urls)} URL:\n{urls_str}")
        else:
            err = await m.reply_text("No URLs found")
            await asyncio.sleep(10)
            await c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = await m.reply_text(f"Error: {e}")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("getsharelist"))
async def get_all_share_urls(c, m):
    notes = NotesDB()
    await m.reply_chat_action(ChatAction.TYPING)
    if m.from_user.id != 5665225938:
        await m.reply(
            "`Vì vấn đề bảo mật, bạn không có quyền sử dụng lệnh này.`",
            quote=True)
        return
    try:
        urls = notes.all("share")
        if urls:
            urls_str = "\n".join(urls)
            await m.reply_text(f"Tìm thấy {len(urls)} URL:\n{urls_str}")
        else:
            err = await m.reply_text("No URLs found")
            await asyncio.sleep(10)
            await c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = await m.reply_text(f"Error: {e}")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, err.id)

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from db import NotesDB
import asyncio


@Client.on_message(filters.command("checkifunavailable"))
async def check_all_urls(c, m):
    notes = NotesDB()
    await m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    if m.from_user.id == 5665225938:
        filename = "v2ray"
    try:
        removed_urls = notes.check(filename)
        if removed_urls:
            removed_urls_str = "\n".join(removed_urls)
            await m.reply_text(
                f" Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}")
        else:
            err = await m.reply_text("No URLs were removed")
            await asyncio.sleep(10)
            await c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = await m.reply_text(f"Error: {e}")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("checksharelistifunavailable"))
async def check_all_share_urls(c, m):
    notes = NotesDB()
    await m.reply_chat_action(ChatAction.TYPING)
    if m.from_user.id != 5665225938:
        await m.reply("`Forbidden`", quote=True)
        return
    try:
        removed_urls = notes.check("share")
        if removed_urls:
            removed_urls_str = "\n".join(removed_urls)
            await m.reply_text(
                f" Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}")
        else:
            err = await m.reply_text("No URLs were removed")
            await asyncio.sleep(10)
            await c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = await m.reply_text(f"Error: {e}")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, err.id)

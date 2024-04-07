from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from db import NotesDB
import asyncio
import re


@Client.on_message(filters.command("add"))
async def add_url(c, m):
    notes = NotesDB()
    await m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    if m.from_user.id == 5665225938:
        filename = "v2ray"
    text = m.text
    if m.reply_to_message:
        text = m.reply_to_message.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )
    if not urls:
        err = await m.reply_text("Vui lòng cung cấp URL")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, err.id)
        await m.delete()
        return
    li = 0
    for url in urls:
        try:
            notes.add(filename, url)
            li += 1
        except Exception as e:
            pass
    if li != len(urls):
        x = len(urls) - li
        temp = await m.reply(f"{x} URL trùng lặp sẽ không được thêm lại")
        await asyncio.sleep(5)
        await c.delete_messages(m.chat.id, temp.id)
    done = await m.reply_text(f"Đã thêm {li} URL")
    await asyncio.sleep(10)
    await c.delete_messages(m.chat.id, done.id)
    await m.delete()


@Client.on_message(filters.command("share"))
async def share_url(c, m):
    notes = NotesDB()
    await m.reply_chat_action(ChatAction.TYPING)
    text = m.text
    if m.reply_to_message:
        text = m.reply_to_message.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )
    if not urls:
        err = await m.reply_text("Vui lòng cung cấp URL")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, err.id)
        return
    li = 0
    for url in urls:
        try:
            notes.add("share", url)
            li += 1
        except Exception as e:
            pass
    if li != len(urls):
        x = len(urls) - li
        temp = await m.reply(f"{x} URL trùng lặp sẽ không được thêm lại")
        await asyncio.sleep(5)
        await c.delete_messages(m.chat.id, temp.id)
    done = await m.reply_text(f"Đã thêm {li} URL")
    await asyncio.sleep(10)
    await done.delete()

import os
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from sub_task import kv

v2tool = os.getenv("v2tool")


@Client.on_message(filters.command("get"))
async def get_urls(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    last_update = kv.get("last_update")
    now = datetime.now()
    diff = now - last_update

    if diff.days > 0:
        time_text = f"{diff.days} ngày trước"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        time_text = f"{hours} giờ trước"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        time_text = f"{minutes} phút trước"
    else:
        time_text = f"{diff.seconds} giây trước"

    text = [
        f"**Link Chuẩn:** {v2tool}/get/default",
        f"**Link Rác:** {v2tool}/get/misc",
        f"**Lần cuối cập nhật: {time_text}**",
    ]
    await m.reply(
        "\n\n".join(text),
        quote=True,
    )

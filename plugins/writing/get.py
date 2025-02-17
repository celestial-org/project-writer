import os
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from sub_task import kv

v2tool = os.getenv("v2tool")


@Client.on_message(filters.command("get"))
async def get_urls(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    last_update = kv.get("last_update")
    text = [
        f"**Link Chuẩn:** {v2tool}/get/default",
        f"**Link Rác:** {v2tool}/get/misc",
        f"**Lần cuối cập nhật: {last_update}**",
    ]
    await m.reply(
        "\n\n".join(text),
        quote=True,
    )

import os
from pyrogram import Client, filters
from pyrogram.enums import ChatAction

v2tool = os.getenv("V2TOOL")


@Client.on_message(filters.command("get"))
async def get_urls(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    text = [
        f"**Shared Link:** {v2tool}/get/share",
        f"**Misc Link:** {v2tool}/get/misc",
        "Các server sẽ tự động được làm mới.",
    ]
    await m.reply(
        "\n\n".join(text),
        quote=True,
    )

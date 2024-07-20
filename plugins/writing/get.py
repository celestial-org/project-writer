import os
from pyrogram import Client, filters
from pyrogram.enums import ChatAction

v2tool = os.getenv("V2TOOL")


@Client.on_message(filters.command("get"))
def get_urls(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    text = [
        f"**Shared Link:** {v2tool}/get/share",
        f"**Misc Link:** {v2tool}/get/misc",
        "Các server sẽ tự động được làm mới.",
    ]
    m.reply(
        "\n\n".join(text),
        quote=True,
    )

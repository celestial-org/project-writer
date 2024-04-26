from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from environment import v2tool


@Client.on_message(filters.command("get"))
def get_urls(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    m.reply(
        f"**Share Note**:\n__--{v2tool}/get/share\n**Update Share Note:\n{v2tool}/update/share\n\n**Personal Note**:\n{v2tool}/get/{filename}\n**Update:\n{v2tool}/update/{filename}",
        quote=True,
    )

from hydrogram import Client, filters
from hydrogram.enums import ChatAction

@Client.on_message(filters.command("helps"))
async def help_list(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    with open("text/helps.md") as f:
        text = f.read()
    text = text.replace("{first_name}", m.from_user.first_name)
    text = text.replace("{uid}", str(m.from_user.id))
    await m.reply(text, quote=True)
    
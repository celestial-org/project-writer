from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from datetime import datetime, timedelta


@Client.on_message(filters.command(["kick", "kickme"]))
def ban_chat_member(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    try:
        m.chat.ban_member(
            m.from_user.id, until_date=datetime.now() + timedelta(seconds=30)
        )
        m.reply("**OK**, __--nguyện vọng đã được thực hiện--__", quote=True)
    except:
        pass

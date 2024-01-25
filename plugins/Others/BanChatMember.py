from pyrogram import Client, filters

@Client.on_message(filters.command(["kick","kickme"]))
def ban_chat_member(c, m):
    try:
        m.chat.ban_member(m.from_user.id)
        m.reply("**OK**, __--nguyện vọng đã được thực hiện--__", quote=True)
    except:
        pass
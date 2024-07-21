from pyrogram import Client, filters
from pyrogram.enums import ChatAction


@Client.on_message(filters.command(["start", "help"]))
def send_welcome(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    m.reply_text(
        f"Xin chào {m.from_user.first_name}(`{m.from_user.id}`)",
        quote=True,
    )


@Client.on_message(filters.command("helps"))
def help_list(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    with open("text/helps.md", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("{first_name}", m.from_user.first_name)
    text = text.replace("{uid}", str(m.from_user.id))
    m.reply(text, quote=True)


@Client.on_message(filters.command("ext"))
def ext_command_list(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    with open("text/ext.md", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("{first_name}", m.from_user.first_name)
    text = text.replace("{uid}", str(m.from_user.id))
    m.reply(text, quote=True)

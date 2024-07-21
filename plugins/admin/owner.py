from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from database.local import kv


def is_owner(_, __, m):
    return m.from_user.id in kv.get("owners")


@Client.on_message(filters.command("add_owner") & filters.create(is_owner))
def add_owner(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if m.reply_to_message:
        user = m.reply_to_message.from_user
        kv["owners"].add(user.id)
    if len(m.command) > 1:
        user = c.get_users(m.command[1])
        kv["owners"].add(user.id)
    m.reply("Xong", quote=True)


@Client.on_message(filters.command("remove_owner") & filters.create(is_owner))
def remove_owner(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if m.reply_to_message:
        user = m.reply_to_message.from_user
        kv["owners"].remove(user.id)
    if len(m.command) > 1:
        user = c.get_users(m.command[1])
        kv["owners"].remove(user.id)
    m.reply("Xong", quote=True)

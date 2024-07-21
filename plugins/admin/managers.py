from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from database import ManagerDB
from database.local import kv


def is_owner(_, __, m):
    return m.from_user.id in kv.get("owners")


@Client.on_message(filters.command("add_manager") & filters.create(is_owner))
def add_manager(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    db = ManagerDB()
    if m.reply_to_message:
        user = m.reply_to_message.from_user
        db.add(user)
    if len(m.command) > 1:
        user = c.get_users(m.command[1])
        db.add(user)
    m.reply("Xong", quote=True)
    kv["managers"].add(user.id)


@Client.on_message(filters.command("remove_manager") & filters.create(is_owner))
def remove_manager(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    db = ManagerDB()
    if m.reply_to_message:
        user = m.reply_to_message.from_user
        db.remove(user)
    if len(m.command) > 1:
        user = c.get_users(m.command[1])
        db.remove(user)
    m.reply("Xong", quote=True)
    kv["managers"].remove(user.id)

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from database.note_manage import NoteManage
from .admin import admin


@Client.on_message(filters.user(admin) & filters.command("add_manager"))
def add_manager(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    db = NoteManage()
    if m.reply_to_message:
        user = m.reply_to_message.from_user
        db.add(user)
    if len(m.command) > 1:
        user = m.chat.get_member(m.command[1])
        db.add(user)
    m.reply("Xong", quote=True)


@Client.on_message(filters.user(admin) & filters.command("del_manager"))
def remove_manager(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    db = NoteManage()
    if m.reply_to_message:
        user = m.reply_to_message.from_user
        db.remove(user)
    if len(m.command) > 1:
        user = c.get_users(m.command[1])
        db.remove(user)
    m.reply("Xong", quote=True)

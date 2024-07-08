from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from database import SSH


@Client.on_message(filters.command("delssh"))
def delete_machine_server(c, m):
    ssh = SSH(m.from_user.id)
    m.reply_chat_action(ChatAction.TYPING)
    try:
        if len(m.command) < 2:
            raise Exception("Vui lòng cung cấp tên máy")
        machine = m.command[1]
        try:
            ssh.delete(machine)
        except Exception as e:
            raise Exception(str(e))
        m.reply(f"Đã xoá máy chủ {machine}", quote=True)
    except Exception as e:
        m.reply(str(e), quote=True)

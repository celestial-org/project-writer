from hydrogram import Client, filters, enums
from hydrogram.enums import ChatAction
from db import SSH


@Client.on_message(filters.command("delssh"))
async def delete_machine_server(c, m):
    ssh = SSH(m.from_user.id)
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        if len(m.command) < 2:
            raise Exception("Vui lòng cung cấp tên máy")
        machine = m.command[1]
        try:
            ssh.delete(machine)
        except Exception as e:
            raise Exception(str(e))
        await m.reply(f"Đã xoá máy chủ {machine}", quote=True)
    except Exception as e:
        await m.reply(str(e), quote=True)

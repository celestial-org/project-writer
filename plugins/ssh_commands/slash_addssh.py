from hydrogram import Client, filters, enums
from hydrogram.enums import ChatAction
from db import SSH
import asyncio

@Client.on_message(filters.command("addssh"))
async def save_ssh_login(c, m):
    ssh = SSH(m.from_user.id)
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        if m.chat.type != enums.ChatType.PRIVATE:
            raise Exception(
                "Để bảo mật, vui lòng thực hiện thao tác này ở chat riêng tư"
            )
        if len(m.command) < 5:
            raise Exception(
                "Không đủ tham số\nVui lòng thực hiện theo mẫu:\n/addserver + `machine name` + `hostname/ip` + `ssh user` + `ssh password` + `ssh port(nếu là 22 thì không cần nhập)`"
            )
        if len(m.command) == 5:
            _, machine, host, sshuser, passwd = m.command
            port = 22
        else:
            _, machine, host, sshuser, passwd, port = m.command
        ssh.add(machine, host, sshuser, passwd, port)
        await m.reply(f"Máy chủ với tên {machine} đã được lưu", quote=True)
        await asyncio.sleep(10)
    except Exception as e:
        await m.reply(str(e), quote=True)
        
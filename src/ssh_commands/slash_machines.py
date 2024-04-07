from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from src.db import SSH
import asyncio


@Client.on_message(filters.command("machines"))
async def get_list_machines(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        user_id = m.from_user.id
        ssh = SSH(user_id)
        user = m.from_user.first_name
        list_machines = ssh.machines(user_id)
        list_machines = "    ".join(list_machines)
        await m.reply(
            f"Danh sách máy chủ SSH của **{user}**:```Machines\n{list_machines}\n```",
            quote=True,
        )
    except Exception as e:
        stt = await m.reply(str(e), quote=True)
        await asyncio.sleep(10)
        await stt.delete()

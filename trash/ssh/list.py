import time
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from database import SSH


@Client.on_message(filters.command("machines"))
def get_list_machines(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    try:
        user_id = m.from_user.id
        ssh = SSH(user_id)
        user = m.from_user.first_name
        list_machines = ssh.machines()
        list_machines = "    ".join(list_machines)
        m.reply(
            f"Danh sách máy chủ SSH của **{user}**:```Machines\n{list_machines}\n```",
            quote=True,
        )
    except Exception as e:
        stt = m.reply(str(e), quote=True)
        time.sleep(10)
        stt.delete()

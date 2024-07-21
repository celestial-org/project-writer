import subprocess
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from database.local import kv


def is_owner(_, __, m):
    return m.from_user.id in kv.get("owners")


@Client.on_message(filters.command("bash") & filters.create(is_owner))
def run_shell_bash(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    command = m.text.replace("/bash ", "")
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        shell=True,
        check=True,
    )
    m.reply(f"```bash\n{result.stdout}\n```")

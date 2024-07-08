import subprocess

from pyrogram import Client, filters
from pyrogram.enums import ChatAction

from .admin import admin


@Client.on_message(filters.command("bash") & filters.user(admin))
def run_shell_bash(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    command = m.text.replace("/bash ", "")
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True
    )
    m.reply(f"```bash\n{result.stdout}\n```")

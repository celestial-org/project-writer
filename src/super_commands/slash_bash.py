from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from .admin import admin
import subprocess


@Client.on_message(filters.command("bash") & filters.user(admin))
async def run_shell_bash(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    command = m.text.replace("/bash ", "")
    result = subprocess.run(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            shell=True)
    await m.reply(f"```bash\n{result.stdout}\n```")

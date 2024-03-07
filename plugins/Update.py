from hydrogram import Client, filters
from hydrogram.enums import ChatAction
import os, sys, requests
from lib.env import server_test
import subprocess

@Client.on_message(filters.command("reset") & filters.user(5665225938))
def reset_program(c, m):
    m.reply("Đang khởi động lại chương trình Client...")
    with open("reset.txt", "w") as f:
        f.write(str(m.chat.id))
    os.execl(sys.executable, sys.executable, *sys.argv)
    
@Client.on_message(filters.command("update") & filters.user(5665225938))
def update_server(c, m):
    m.reply("Đang cập nhật hệ thống...")
    os.system('git config --global pull.rebase true')
    os.system('git config --global user.name "Writer"')
    os.system('git config --global user.email "duongchantroi@alwaysdata.net"')
    os.system('git config --global pull.rebase true')
    os.system("git add * && git commit -a -m UPDATE")
    os.system("git pull")
    m.reply("Đã cập nhật xong")#, đang khởi động lại...")
   # with open("reset.txt", "w") as f:
       # f.write(str(m.chat.id))
    #os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("rerunapi") & filters.user(5665225938))
def reset_api_server(c, m):
    m.reply("Đã bắt đầu khởi động lại API", quote=True)
    try:
        requests.post(f"{server_test}/reset", timeout=10)
    except Exception:
        pass
    
@Client.on_message(filters.command("updateapi") & filters.user(5665225938))
def update_api_server(c, m):
    m.reply("Đã bắt đầu cập nhật API", quote=True)
    try:
        requests.post(f"{server_test}/update", timeout=10)
    except Exception:
        pass
    
@Client.on_message(filters.command("bash") & filters.user(5665225938))
def run_shell_bash(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    command = m.text.replace("/bash ", "")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    m.reply(f"```bash\n{result.stdout}\n```")
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from lib.env import config_tool


@Client.on_message(filters.command("helps"))
def help_list(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    with open("plugins/text/helps.txt") as f:
        text = f.read()
    text = text.replace("{first_name}", m.from_user.first_name)
    text = text.replace("{uid}", str(m.from_user.id))
    m.reply(text, quote=True)


@Client.on_message(filters.command("ext"))
def ext_command_list(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    with open("plugins/text/ext.md") as f:
        text = f.read()
    text = text.replace("{first_name}", m.from_user.first_name)
    text = text.replace("{uid}", str(m.from_user.id))
    m.reply(text, quote=True)


@Client.on_message(filters.command("install"))
def help_install_endpoint(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    m.reply(
        "**Thiết lập với Docker:**\n`docker run -e PREFIX=(nhập prefix vào đây) -e NAME=(nhập tên vào đây) -d ghcr.io/bosuutap/writer-endpoint:main`\n\n**Thiết lập thủ công:**\n`git clone https://github.com/bosuutap/writer-endpoint && cd writer-endpoint && pip install -r requirements.txt && bash setup.sh`\n\n**Sau đó chạy bằng lệnh:** `python start.py (nhập prefix vào đây) (tên của bạn vào đây)`",
        quote=True,
    )


@Client.on_message(filters.command(["start", "help"]))
def send_welcome(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    m.reply_text(
        f"Xin chào {m.from_user.first_name}(`{m.from_user.id}`)\nDùng lệnh /helps để biết thêm chi tiết",
        quote=True,
    )

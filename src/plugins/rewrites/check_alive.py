import concurrent.futures
import requests
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from environment import test_server
from .test import get_config


def check_alive(config):
    check_tool = f"{test_server}/check"
    r = requests.get(check_tool, params={"q": config})
    response = r.json()
    return response.get("alive", False)


def generate_link(item_list):
    data = "\n".join(item_list)
    r = requests.post("https://paste.rs/", data=data)
    return r.text


@Client.on_message(filters.command("filter_alive"))
def filter_alive(c, m):
    """
    command function
    """
    user = m.from_user.first_name if m.from_user else m.sender_chat.title
    m.reply_chat_action(ChatAction.TYPING)
    if m.reply_to_message:
        mpath = m.reply_to_message.text.split()
        urls = [
            part
            for part in mpath
            if any(part.startswith(scheme) for scheme in ["http://", "https://"])
        ]
    else:
        urls = [
            part
            for part in m.command
            if any(part.startswith(scheme) for scheme in ["http://", "https://"])
        ]

    if not urls:
        m.reply("```\nKhong tim thay URL```", quote=True)
        return

    def handler(url):
        try:
            test_url, count = get_config(url)
        except:
            m.reply(f"```Lien ket {url} khong kha dung```", quote=True)
            return

        text = f"**{user}** đang lọc subscription {url} với {count} server"
        tmp = m.reply(text, quote=True)
        response = requests.get(test_url, timeout=120)
        configs = response.text.splitlines()
        alive_list = []
        dead_list = []
        for config in configs:
            if check_alive(config):
                alive_list.append(config)
            else:
                dead_list.append(config)

        alive_link = generate_link(alive_list)
        dead_count = len(dead_list)
        text = [
            f"Original: {url}",
            f"Kết quả: {alive_link}",
            f"Đã xóa {dead_count} liên kết",
            f"Sender **{user}**",
        ]
        text = "\n".join(text)
        m.reply(text, quote=True)
        tmp.delete()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(handler, urls)

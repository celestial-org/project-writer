import re
import os
import concurrent.futures
import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from utils.other import get_config

test_server = os.getenv("TEST_SERVER")


def start_test(config):
    try:
        r = requests.post(test_server, json={"q": config}, timeout=60)
        return r.text
    except Exception as e:
        print(e)
        return ""


@Client.on_message(filters.command("test"))
def litespeedtest(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    url_pattern = re.compile(
        r"((http[s]?|vmess|trojan|vless|ss)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
    )
    if m.reply_to_message:
        try:
            text = m.reply_to_message.text
        except Exception:
            try:
                text = m.reply_to_message.caption
            except Exception:
                m.reply("Không tìm thấy tin nhắn văn bản", quote=True)
                return
    else:
        try:
            text = m.text
        except Exception:
            try:
                text = m.caption
            except Exception:
                m.reply("Không tìm thấy tin nhắn văn bản", quote=True)
                return
    matches = re.findall(url_pattern, text)
    urls = [match[0] for match in matches]
    if not urls:
        m.reply("Không tìm thấy URL trong tin nhắn văn bản", quote=True)
        return

    def handler(url):
        m.reply_chat_action(ChatAction.TYPING)
        try:
            url, configs, count = get_config(url)
        except Exception:
            m.reply(f"Liên kết {url} không khả dụng", quote=True)
            return
        if count is None:
            m.reply(f"Liên kết {url} không có máy chủ nào cả !", quote=True)
            return

        s_msg = m
        first_msg = m
        result_good = ""
        result_none = ""
        count = 0
        for config in configs:
            result = start_test(config)
            if "|" not in result:
                continue
            if "N/A" in result:
                result_none = f"{result_none}{result}\n"
            else:
                result_good = f"{result_good}{result}\n"
            result_gather = result_good + result_none
            s_text = (
                f"{url}"
                + f"\nTest bởi <b><a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a></b>"
                + "<pre><code>"
                + result_gather
                + "</code></pre>"
            )
            if count > 1:
                s_text = (
                    "<b>"
                    + str(count)
                    + "</b>"
                    + "<pre><code>"
                    + result_gather
                    + "</code></pre>"
                )
            try:
                s_msg.edit(s_text, parse_mode=ParseMode.HTML)
            except Exception as e:
                print(e)
                result_gather = result + "\n"
                s_msg = first_msg.reply(s_text, quote=True, parse_mode=ParseMode.HTML)
                count += 1
                if count == 1:
                    first_msg = s_msg
        result_gather = ""
        s_msg = None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(handler, urls)

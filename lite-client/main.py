import os
import re
import json
import base64
import subprocess
import concurrent.futures
import requests
from pyrogram import Client, filters, idle
from pyrogram.enums import ChatAction, ParseMode


bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    print("Please provide BOT_TOKEN as an environment variable", flush=True)
app = Client(
    "lite_client",
    21021245,
    "7b32ea92719781c5e22ede319c5dbde5",
    bot_token=bot_token,
    in_memory=True,
)


def get_config(data):
    url = data
    if any(
        data.startswith(sche) for sche in ["vmess://", "trojan://", "vless://", "ss://"]
    ):
        url = requests.post(
            "https://paste.rs",
            data=data,
            timeout=20,
            headers={"Content-Type": "text/plain"},
        ).text
    elif any(data.startswith(sche) for sche in ["http", "https"]):
        req = requests.get(
            data,
            headers={"User-Agent": "v2rayNG/1"},
            proxies={
                "http": "http://127.0.0.1:6868",
                "https": "http://127.0.0.1:6868",
            },
            timeout=20,
        )
        data = req.text
        if not any(
            data.startswith(sche) for sche in ["vmess", "trojan", "vless", "ss:"]
        ):
            data = base64.b64decode(data).decode()
    else:
        data = base64.b64decode(data).decode()
    data = data.split()
    count = len(data)
    return url, data, count


def lite(config):
    try:
        out = subprocess.check_output(
            ["./lite", "-config", "config.json", "-test", config],
            stderr=subprocess.STDOUT,
            text=True,
        )
        out_lines = out.splitlines()
        res = [line for line in out_lines if "gotspeed" in line]
        if len(res) > 1:
            res = res[-1]
        else:
            res = res[0]
        result_json = res[res.find("{") : res.rfind("}") + 1]
        result = json.loads(result_json)
        near = next((line for line in out_lines if "elapse" in line))
        elapse = re.search(r"elapse: (\d+)ms", near).group(1)
        tag = near.split(" 0 ")[1].split(" elapse")[0]
        avg_speed = result["speed"]
        max_speed = result["maxspeed"]
        return f"{tag}\n🔄{elapse}ms|🟰{avg_speed}|⚡{max_speed}"
    except subprocess.CalledProcessError as e:
        print(e)
        return "N/A"


@app.on_message(filters.command("start"))
def start_command(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    m.reply("🚀 Lite Speed Test bot", quote=True)


def start_test(config):
    try:
        return lite(config)
    except Exception as e:
        print(e)
        return "N/A"


@app.on_message(filters.command("test"))
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


app.start()
print("Lite Speed Test bot started")
idle()
app.stop()
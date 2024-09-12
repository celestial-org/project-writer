import time
import random
import string
import base64
import concurrent.futures
from datetime import datetime

import pytz
import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode


def generate_id(length=12):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for i in range(length))
    return random_string


def convert_bytes_to_human_readable(bytes_value):
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    unit_index = 0

    while bytes_value >= 1024 and unit_index < len(units) - 1:
        bytes_value /= 1024.0
        unit_index += 1

    result = "{:.2f} {}".format(bytes_value, units[unit_index])
    return result


def convert_timestamp_to_datetime(timestamp, timezone="UTC"):
    utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    local_datetime = utc_datetime.astimezone(pytz.timezone(timezone))
    return local_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")


def parse_url(url):
    try:
        r = requests.get(
            url,
            headers={"User-Agent": "quantumult%20x"},
            proxies={"http": "http://127.0.0.1:6868", "https": "http://127.0.0.1:6868"},
            timeout=30,
        )
        res_string = r.headers.get("subscription-userinfo")
    except Exception:
        r = requests.get(url, headers={"User-Agent": "quantumult%20x"}, timeout=30)
        res_string = r.headers.get("subscription-userinfo")
    res_text = r.text
    if "{" in res_text or not res_text:
        raise Exception("Unavailable")
    try:
        res_text = base64.b64decode(res_text.encode("utf-8")).decode("utf-8")
    except Exception:
        pass
    result_dict = {}
    orgi_dict = {}
    if res_string:
        pairs = res_string.split("; ")
        for pair in pairs:
            key, value = pair.split("=")
            if key in ["upload", "download", "total"]:
                orgi_dict[key] = value
                value = convert_bytes_to_human_readable(float(value))
            elif key == "expire":
                try:
                    value = convert_timestamp_to_datetime(
                        int(value), timezone="Asia/Ho_Chi_Minh"
                    )
                except Exception:
                    value = "khong xac dinh"
            result_dict[key] = value
        if (
            "upload" in result_dict
            and "download" in result_dict
            and "total" in result_dict
        ):
            available = int(orgi_dict["total"]) - (
                int(orgi_dict["upload"]) + int(orgi_dict["download"])
            )
            result_dict["available"] = convert_bytes_to_human_readable(available)
    return result_dict, len(res_text.splitlines())


@Client.on_message(
    (filters.command("check") & filters.private) | filters.regex("check@writerplus_bot")
)
def check_sub(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if m.reply_to_message and m.reply_to_message.text:
        text = m.reply_to_message.text
    elif m.text:
        text = m.text
    else:
        m.reply("Không tìm thấy tin nhắn", quote=True)
        return False
    urls = [
        url
        for url in text.split(None)
        if any(scheme in url for scheme in ["http://", "https://"])
    ]
    if not urls:
        m.reply("URL là cần thiết để kiểm tra", quote=True)
        return False
    try:
        user = m.from_user.first_name
    except Exception as e:
        print(e)
        user = m.sender_chat.title
    sleep = 1

    def handler(url):
        nonlocal sleep
        time.sleep(sleep)
        sleep += 1
        m.reply_chat_action(ChatAction.TYPING)
        try:
            info, count = parse_url(url)
        except Exception:
            message = f"{url}\nCheck bởi <b>{user}</b>\n<b>Subscription lỗi</b>"
            m.reply(message, quote=True)
            return True
        if info and all(
            key in info
            for key in ["total", "upload", "download", "available", "expire"]
        ):
            total = info.get("total", "N/A")
            upl = info.get("upload", "N/A")
            downl = info.get("download", "N/A")
            avail = info.get("available", "N/A")
            expire = info.get("expire", "N/A")

            message = (
                f"{url}\n"
                f"Check bởi <b>{user}</b>\n"
                f"Số lượng cấu hình: <b>{count}</b>\n"
                f"Tổng: <b>{total}</b>\n"
                f"Đã dùng: <b>↑{upl}, ↓{downl}</b>\n"
                f"Còn lại: <b>{avail}</b>\n"
                f"Hết hạn: <b>{expire}</b>"
            )
        else:
            message = (
                f"{url}\nCheck bởi <b>{user}</b>\nSố lượng cấu hình: <b>{count}</b>"
            )

        m.reply(message, quote=True, parse_mode=ParseMode.HTML)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(handler, urls)

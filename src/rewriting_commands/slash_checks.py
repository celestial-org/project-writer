from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from datetime import datetime
import pytz
import requests
import base64
import asyncio


async def convert_bytes_to_human_readable(bytes_value):
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0

    while bytes_value >= 1024 and unit_index < len(units) - 1:
        bytes_value /= 1024.0
        unit_index += 1

    result = "{:.2f} {}".format(bytes_value, units[unit_index])
    return result


async def convert_timestamp_to_datetime(timestamp, timezone="UTC"):
    utc_datetime = datetime.utcfromtimestamp(timestamp).replace(
        tzinfo=pytz.utc)
    local_datetime = utc_datetime.astimezone(pytz.timezone(timezone))
    return local_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")


async def parse_url(url):
    try:
        r = requests.get(
            url,
            headers={"User-Agent": "quantumult%20x"},
            proxies={
                "http": "http://127.0.0.1:8888",
                "https": "http://127.0.0.1:8888"
            },
            timeout=30,
        )
        res_string = r.headers.get("subscription-userinfo")
    except Exception:
        r = requests.get(url,
                         headers={"User-Agent": "quantumult%20x"},
                         timeout=30)
        res_string = r.headers.get("subscription-userinfo")
    res_text = r.text
    if "{" in res_text or not res_text:
        raise Exception("Unavailable")
    try:
        res_text = base64.b64decode(res_text)
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
                value = await convert_bytes_to_human_readable(float(value))
            elif key == "expire":
                try:
                    value = await convert_timestamp_to_datetime(
                        int(value), timezone="Asia/Ho_Chi_Minh")
                except:
                    value = "khong xac dinh"
            result_dict[key] = value
        if ("upload" in result_dict and "download" in result_dict
                and "total" in result_dict):
            available = int(orgi_dict["total"]) - (int(orgi_dict["upload"]) +
                                                   int(orgi_dict["download"]))
            result_dict["available"] = await convert_bytes_to_human_readable(
                available)
    return result_dict, len(res_text.splitlines())


@Client.on_message(filters.command("checks"))
async def check_sub(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    if m.reply_to_message and m.reply_to_message.text:
        text = m.reply_to_message.text
    elif m.text:
        text = m.text
    else:
        await m.reply("Không tìm thấy tin nhắn", quote=True)
        return False
    urls = [
        url for url in text.split(None)
        if any(scheme in url for scheme in ["http://", "https://"])
    ]
    if not urls:
        await m.reply("URL là cần thiết để kiểm tra", quote=True)
        return False
    try:
        user = m.from_user.first_name
    except Exception:
        user = m.sender_chat.title

    async def handler(url):
        await m.reply_chat_action(ChatAction.TYPING)
        try:
            info, count = await parse_url(url)
        except Exception:
            message = f"{url}\n**__Check bởi__ --{user}--**\n__--**Subscription lỗi**--"
            await m.reply(message, quote=True)
            return True
        if info and all(
                key in info for key in
            ["total", "upload", "download", "available", "expire"]):
            total = info.get("total", "N/A")
            upl = info.get("upload", "N/A")
            downl = info.get("download", "N/A")
            avail = info.get("available", "N/A")
            expire = info.get("expire", "N/A")

            message = (f"{url}\n"
                       f"**__Check bởi__ --{user}--**\n"
                       f"__**Số lượng cấu hình:**__ --{count}--\n"
                       f"**Tổng:** --{total}--\n"
                       f"**Đã dùng:** ↑--{upl}--, ↓--{downl}--\n"
                       f"**Còn lại:** --{avail}--\n"
                       f"**Hết hạn:** __--{expire}--__")
        else:
            message = f"{url}\n**__Check bởi__ --{user}--**\n__**Số lượng cấu hình:**__ --{count}--"

        await m.reply(message, quote=True)

    async def main(urls):
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(handler(url)))
        await asyncio.gather(*tasks)

    await main(urls)

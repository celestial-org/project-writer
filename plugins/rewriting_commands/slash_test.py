from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from environment import test_server
import requests
import asyncio
import re
import base64


async def get_config(url):
    if any(scheme in url for scheme in ["vmess:", "trojan:", "vless:", "ss:"]):
        res = url
        url = requests.post("https://paste.rs/", data=url).text
    else:
        res = requests.get(
            url,
            headers={"User-Agent": "v2rayNG"},
            timeout=60,
            proxies={
                "http": "http://127.0.0.1:8888",
                "https": "http://127.0.0.1:8888",
            },
        )

        res = res.text
        if not any(
                res.startswith(sche)
                for sche in ["vmess", "trojan", "vless", "ss://"]):
            res = base64.b64decode(res.encode("utf-8")).decode("utf-8")
            url = requests.post("https://paste.rs/", data=res).text
    count = len(res.splitlines())
    return url, count


async def start_test(config):
    r = requests.post(test_server, json={"q": config})
    return r.text


@Client.on_message(filters.command("test"))
async def litespeedtest(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
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
                await m.reply("Không tìm thấy tin nhắn văn bản", quote=True)
                return
    else:
        try:
            text = m.text
        except Exception:
            try:
                text = m.caption
            except Exception:
                await m.reply("Không tìm thấy tin nhắn văn bản", quote=True)
                return
    matches = re.findall(url_pattern, text)
    urls = [match[0] for match in matches]
    if not urls:
        await m.reply("Không tìm thấy URL trong tin nhắn văn bản", quote=True)
        return

    async def handler(url):
        await m.reply_chat_action(ChatAction.TYPING)
        try:
            test_url, count = await get_config(url)
        except Exception:
            uvl = await m.reply(f"Liên kết {url} không khả dụng", quote=True)
            await asyncio.sleep(10)
            await uvl.delete()
            return
        if count is None:
            await m.reply(f"Liên kết {url} bị lỗi", quote=True)
            return
        if url.startswith("http"):
            stt = await m.reply(
                f"**{m.from_user.first_name}** thực hiện test liên kết {url} với **{count}** cấu hình",
                quote=True,
            )
        else:
            stt = await m.reply(
                f"**{m.from_user.first_name}** thực hiện test 1 cấu hình\n{test_url}",
                quote=True,
            )
            url = test_url
        r = requests.get(test_url)
        configs = r.text.splitlines()
        s_msg = m
        result_gather = ""
        count = 0
        for config in configs:
            result = await start_test(config)
            result_gather = f"{result_gather}{result}\n"
            s_text = (
                url +
                f"\n__Test bởi **[{m.from_user.first_name}](tg://user?id={m.from_user.id})**__"
                + "```\n" + result_gather + "```")
            if count > 1:
                s_text = (url + " **" + str(count) + "**" + "```\n" +
                          result_gather + "```")
            try:
                await s_msg.edit(s_text)
            except Exception:
                result_gather = result + "\n"
                s_msg = await s_msg.reply(s_text, quote=True)
                count += 1
        result_gather = ""
        s_msg = None
        await stt.delete()

    async def main(urls):
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(handler(url)))
        await asyncio.gather(*tasks)

    await main(urls)

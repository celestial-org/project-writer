from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from db import endpoints as ep
from lib.lite import get_config, start_test, check_before
import re
import time
import requests

url_pattern = re.compile(
    r"((http[s]?|vmess|trojan|vless|ss)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
)


def test_filter(_, __, m):
    return m.text.startswith("/test_") if m.text else False


@Client.on_message(filters.create(test_filter), group=2)
def regex_lite_command(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    command = m.text.split(" ")[0]
    if "@v2writer_bot" in command:
        command = command.replace("@v2writer_bot", "")
    prefix = command.replace("/test_", "")
    try:
        endpoint = check_before(prefix)
    except Exception as e:
        m.reply(str(e), quote=True)
        return
    if m.reply_to_message:
        try:
            text = m.reply_to_message.text
        except:
            try:
                text = m.reply_to_message.caption
            except:
                m.reply("Không tìm thấy tin nhắn văn bản", quote=True)
                return
    else:
        try:
            text = m.text
        except:
            try:
                text = m.caption
            except:
                m.reply("Không tìm thấy tin nhắn văn bản", quote=True)
                return
    matches = re.findall(url_pattern, text)
    urls = [match[0] for match in matches]
    if not urls:
        m.reply("Không tìm thấy URL trong tin nhắn văn bản", quote=True)
        return
    for url in urls:
        try:
            test_url, count = get_config(url)
        except:
            uvl = m.reply("Liên kết không khả dụng", quote=True)
            time.sleep(10)
            uvl.delete()
            return
        if count is None:
            m.reply("Liên kết bị lỗi", quote=True)
            return
        if url.startswith("http"):
            stt = m.reply(
                f"**{m.from_user.first_name}** thực hiện test liên kết {url} với **{count}** cấu hình\nPrefix: **{prefix.upper()}**",
                quote=True,
            )
        else:
            stt = m.reply(
                f"**{m.from_user.first_name}** thực hiện test 1 cấu hình\n{test_url}\nPrefix: **{prefix.upper()}**",
                quote=True,
            )
        try:
            location, org, sponsor, photo = start_test(test_url, endpoint)
        except Exception as e:
            m.reply(f"**Lỗi máy chủ:** ```{e}```")
            return
        m.reply_photo(
            photo=photo,
            quote=True,
            caption=f"```sponsor\n{sponsor}\n```\nVị trí: **{location}**\nTổ chức: **{org}**\nTest bởi **[{m.from_user.first_name}](tg://user?id={m.from_user.id})**",
        )
        time.sleep(5)
        stt.delete()

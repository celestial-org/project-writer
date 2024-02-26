from hydrogram import Client, filters
from lib.lite import get_config, start_test, get_endpoints, check_before, start_v2
from hydrogram.enums import ChatAction
import subprocess
import time
import requests
import base64
import os
import re
import random

def ranpoint():
    _, epoints,__ = get_endpoints()
    return random.choice(epoints)

@Client.on_message(filters.command("test"))
def test_v2(c, m):
    m.reply_chat_action(ChatAction.TYPING)    
    url_pattern = re.compile(r'((http[s]?|vmess|trojan|vless|ss)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
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
        m.reply_chat_action(ChatAction.TYPING)
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
            stt = m.reply(f'**{m.from_user.first_name}** thực hiện test liên kết {url} với **{count}** cấu hình', quote=True)
        else:
            stt = m.reply(f'**{m.from_user.first_name}** thực hiện test 1 cấu hình\n{test_url}', quote=True)
        r = requests.get(test_url)
        configs = r.text.splitlines()
        s_msg = None
        pre_conf = []
        for config in configs:
            result = start_v2(config)
            pre_conf.append(result)
            if not s_msg:
                s_msg = m.reply("```\n"+result+"```", quote=True)
            else:
                try:
                    s_msg.edit("```\n"+"\n".join(pre_conf)+"```"+f"__Test bởi **[{m.from_user.first_name}](tg://user?id={m.from_user.id})**__")
                except:
                    pre_conf = []
                    s_msg = m.reply("```\n"+result+"```", quote=True)
        return
        results = [start_v2(config) for config in configs]
        current_chunk = []
        total_chars = 0
        for result in results:
            result_length = len(result)
            if total_chars + result_length <= 4000:
                current_chunk.append(result)
                total_chars += result_length
            else:
                m.reply("```\n"+"\n".join(current_chunk)+"```", quote=True)
                current_chunk = [result]
                total_chars = result_length
        if current_chunk:
            m.reply("```\n"+"\n".join(current_chunk)+"```"+f"__Test bởi **[{m.from_user.first_name}](tg://user?id={m.from_user.id})**__", quote=True)
        stt.delete()

#drop
def run_lite_command(c, m):
    m.reply_chat_action(ChatAction.TYPING)    
    prefix = os.getenv("ENDPOINT")
    url_pattern = re.compile(r'((http[s]?|vmess|trojan|vless|ss)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
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
        m.reply_chat_action(ChatAction.TYPING)
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
        if not prefix:
            try:
                prefix = ranpoint()
            except:
                m.reply("Không có máy chủ test nào hoạt động cả", quote=True)
                return
        try:
            endpoint = check_before(prefix)
        except Exception as e:
            stt = m.reply(f"{e}. Hãy thử máy chủ test khác", quote=True)
            time.sleep(10)
            stt.delete()
            return
        if url.startswith("http"):
            stt = m.reply(f'**{m.from_user.first_name}** thực hiện test liên kết {url} với **{count}** cấu hình\nPrefix: **{prefix.upper()}**', quote=True)
        else:
            stt = m.reply(f'**{m.from_user.first_name}** thực hiện test 1 cấu hình\n{test_url}\nPrefix: **{prefix.upper()}**', quote=True)
        try:
            location, org, sponsor, photo = start_test(test_url, endpoint)
        except Exception as e:
            m.reply(f"**Lỗi máy chủ:** ```{e}```")
            return
        m.reply_photo(photo=photo, quote=True, caption=f"```sponsor\n{sponsor}\n```\nVị trí: **{location}**\nTổ chức: **{org}**\nTest bởi **[{m.from_user.first_name}](tg://user?id={m.from_user.id})**")
        time.sleep(5)
        stt.delete()
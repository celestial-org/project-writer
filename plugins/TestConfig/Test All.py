from hydrogram import Client, filters, enums
from hydrogram.enums import ChatAction
from lib.lite import get_config, start_test, check_before, get_endpoints
from db import endpoints as eps
import subprocess
import time
import requests
import base64
import os
import re

def _admin(_, __, m):
    if m.chat.type != enums.ChatType.PRIVATE:
        member = m.chat.get_member(m.from_user.id)
        bot = m.chat.get_member(6580709427)
        return member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR] and bot.status == enums.ChatMemberStatus.ADMINISTRATOR
    else:
        return m.from_user.id == 5665225938

@Client.on_message(filters.command("testall") & filters.create(_admin))
def run_lite_command_test_all(c, m):
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
        stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến liên kết {url} với **{count}** cấu hình.\n**ALL**', quote=True)
    else:
        stt = m.reply(f'**{m.from_user.first_name}** vừa bắt đầu đợt kiểm tra mới đến 1 cấu hình\n{test_url}.\nMáy chủ test: **ALL**', quote=True)
    _, endpoints, __ = get_endpoints()
    msg_list = []
    for prefix in endpoints:
        try:
            endpoint = check_before(prefix)
            location, org, sponsor, photo = start_test(test_url, endpoint)
        except:
            continue
        msg = (photo, f"```sponsor\n{sponsor}\n```\nVị trí: **{location}**\nTổ chức: **{org}**\nTest bởi **[{m.from_user.first_name}](tg://user?id={m.from_user.id})**")
        msg_list.append(msg)
    for msg in msg_list:
        m.reply_chat_action(ChatAction.TYPING)
        m.reply_photo(photo=msg[0], caption=msg[1], quote=True)
    time.sleep(5)
    stt.delete()
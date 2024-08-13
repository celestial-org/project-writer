import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction


@Client.on_message(filters.command("get_headers"))
def get_headers(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) < 2:
        m.reply("Vui long cung cap URL", quote=True)
        return
    url = m.command[1]
    headers = {}
    params = {}
    for part in m.command:
        if "url=" in part:
            url = part.split("url=")[1]
        if "headers=" in part:
            pre_headers = part.split("headers=")[1]
            for header in pre_headers.split(","):
                key, value = header.split(":")
                headers[key] = value
        if "params=" in part:
            params = part.split("params=")[1]
            params = dict(pair.split(":") for pair in params.split(","))

    r = requests.get(url, headers=headers, params=params, timeout=80)
    res_headers = {}
    response = r.headers
    for key, value in response.items():
        res_headers[key] = value
    m.reply(f"{url}```headers\n{res_headers}```", quote=True)


@Client.on_message(filters.command("get_body"))
def get_body(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) < 2:
        m.reply("Vui long cung cap URL", quote=True)
        return
    url = m.command[1]
    headers = {}
    for part in m.command:
        if "url=" in part:
            url = part.split("url=")[1]
        if "headers=" in part:
            pre_headers = part.split("headers=")[1]
            for header in pre_headers.split(","):
                key, value = header.split(":")
                headers[key] = value
        if "params=" in part:
            params = part.split("params=")[1]
            params = dict(pair.split(":") for pair in params.split(","))

    r = requests.get(url, headers=headers, params=params, timeout=80)
    m.reply(f"{url}```body\n{r.text}```", quote=True)


@Client.on_message(filters.command("request_post"))
def request_post(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) < 2:
        m.reply("Vui long cung cap URL", quote=True)
        return
    url = m.command[1]
    headers = {}
    for part in m.command:
        if "url=" in part:
            url = part.split("url=")[1]
        if "headers=" in part:
            pre_headers = part.split("headers=")[1]
            for header in pre_headers.split(","):
                key, value = header.split(":")
                headers[key] = value
        if "json=" in part:
            data = part.split("data=")[1]
            data = dict(pair.split(":") for pair in data.split(","))
    r = requests.post(url, headers=headers, json=data, timeout=80)
    m.reply(f"{url}```body\n{r.text}```", quote=True)


@Client.on_message(filters.command("request_delete"))
def request_delete(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) < 2:
        m.reply("Vui long cung cap URL", quote=True)
        return
    url = m.command[1]
    headers = {}
    for part in m.command:
        if "url=" in part:
            url = part.split("url=")[1]
        if "headers=" in part:
            pre_headers = part.split("headers=")[1]
            for header in pre_headers.split(","):
                key, value = header.split(":")
                headers[key] = value
    r = requests.delete(url, headers=headers, timeout=80)
    m.reply(f"{url}```body\n{r.text}```", quote=True)

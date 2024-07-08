from pyrogram import Client, filters
from pyrogram.enums import ChatAction
import requests


@Client.on_message(filters.command("request"))
def requesting(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) > 1 and m.command[1] in [
            "GET",
            "get",
            "POST",
            "post",
            "DELETE",
            "delete",
    ]:
        method = m.command[1].upper()
    else:
        method = "GET"
    if any(part in ["headers", "body", "picture"] for part in m.command):
        req = [
            part.replace("...", "") for part in m.command
            if any(part in ["headers", "body", "picture"])
        ][0]
    else:
        req = "headers"
    if any(sche in m.text for sche in ["http://", "https://"]):
        text = m.text
    elif any(sche in m.reply_to_message.text
             for sche in ["http://", "https://"]):
        text = m.reply_to_message.text
    for url in [
            url for url in text.split(None)
            if any(scheme in url for scheme in ["http://", "https://"])
    ]:
        r = requests.request(
            method,
            url,
            headers={"User-Agent": "Writer/1"},
            proxies={
                "http": "http://127.0.0.1:8888",
                "https": "http://127.0.0.1:8888"
            },
        )
        headers = "\n".join(
            [f"{k.upper()}: {v}" for k, v in r.headers.items()])
        m.reply(f"```json\n{headers}```", quote=True)

import time
import os
import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from database import NoteDB


def check_urls(urls: list) -> list:
    removed_urls = []
    for url in urls:
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "v2rayNG"},
                proxies={
                    "http": "http://127.0.0.1:6868",
                    "https": "http://127.0.0.1:6868",
                },
                timeout=60,
            )
        except Exception as e:
            print(e)
            removed_urls.append(url)
            continue
        if response.status_code != 200 or response.text is None or "{" in response.text:
            removed_urls.append(url)

    return removed_urls


@Client.on_message(filters.command("checklive"))
def check_all_urls(c, m):
    owner = int(os.getenv("OWNER_ID"))
    if os.getenv("MANAGERS"):
        managers = {int(i) for i in os.getenv("MANAGERS").split(",")}
    else:
        managers = set()
    user_id = m.from_user.id
    notes = NoteDB()
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) > 1:
        filename = m.command[1]
    elif m.from_user.id == owner:
        filename = "v2ray"
    else:
        m.reply(
            "Vui lòng cung cấp tên note <pre>/checklive example_note_name</pre>",
            quote=True,
        )
        return
    if filename == "share":
        if m.from_user.id not in [owner, *managers]:
            m.reply("**You don't have permission to access this note**", quote=True)
            return
    else:
        note = notes.get_note(filename)
        if user_id not in [note.user_id, owner]:
            m.reply("<b>You don't have permission to access this note</b>", quote=True)
            return
    try:
        urls = notes.list_links(filename)
        removed_urls = check_urls(urls)
        for url in removed_urls:
            notes.delete_link(filename, url)
        if removed_urls:
            removed_urls_str = "\n".join(removed_urls)
            m.reply(
                f" Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}",
                quote=True,
                parse_mode=ParseMode.HTML,
            )
        else:
            err = m.reply("No URLs were removed", quote=True)
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)

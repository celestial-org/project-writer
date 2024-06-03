import time
import requests
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from database import NotesDB, NoteManage, Turso


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


@Client.on_message(filters.command("check_alive"))
def check_all_urls(c, m):
    notes = Turso()
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) > 1 and m.command[1].startswith(":"):
        filename = m.command[1].replace(":", "")
    elif m.from_user.id == 5665225938:
        filename = "v2ray"
    else:
        m.reply("Vui lòng cung cấp tên ghi", quote=True)
        return
    try:
        urls = notes.list(filename, m.from_user.id)
        removed_urls = check_urls(urls)
        for url in removed_urls:
            notes.delete(filename, url, m.from_user.id)
        if removed_urls:
            removed_urls_str = "\n".join(removed_urls)
            m.reply(
                f" Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}",
                quote=True,
            )
        else:
            err = m.reply("No URLs were removed", quote=True)
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply_text(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("check_share"))
def check_all_share_urls(c, m):
    notes = Turso()
    managers = NoteManage()
    m.reply_chat_action(ChatAction.TYPING)
    if m.from_user.id != 5665225938 and not managers.get(m.from_user):
        m.reply("`Forbidden`", quote=True)
        return
    try:
        urls = notes.list("share", m.from_user.id)
        removed_urls = check_urls(urls)
        for url in removed_urls:
            notes.delete("share", url, 5665225938)
        if removed_urls:
            removed_urls_str = "\n".join(removed_urls)
            m.reply(
                f" Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}", quote=True
            )
        else:
            err = m.reply("No URLs were removed", quote=True)
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply_text(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)

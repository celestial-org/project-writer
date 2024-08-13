import os
import base64
import random
import requests


def update_note(db, note_title):
    links = set()
    note = db.get_note(note_title)

    def handle(text):
        if not any(
            scheme in text for scheme in ["vmess://", "trojan://", "vless://", "ss://"]
        ):
            text = base64.b64decode(text).decode()
        slinks = text.splitlines()
        for link in slinks:
            if any(
                link.startswith(scheme)
                for scheme in ["vmess://", "trojan://", "vless://", "ss://"]
            ):
                links.add(link)

    urls = note.urls.split("\n")
    random.shuffle(urls)
    for url in urls:
        if url.startswith("http"):
            try:
                req = requests.get(
                url,
                timeout=20,
                headers={"User-Agent": "v2rayNG"},
                proxies={
                    "http": "http://127.0.0.1:6868",
                    "https": "http://127.0.0.1:6868",
                },
            )
                if req.status_code == 200 and req.text is not None:
                    handle(req.text)
            except Exception as e:
                print(e)
    if links:
        note.content = "\n".join(links)
        db.update_note(note)
        print(note.title, " updated")

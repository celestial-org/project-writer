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
            try:
                text = base64.b64decode(text.encode()).decode()
                if not any(
                    scheme in text
                    for scheme in ["vmess://", "trojan://", "vless://", "ss://"]
                ):
                    raise Exception
            except Exception:
                return
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
            if (
                req.status_code == 200
                and "text/plain" in req.headers.get("Content-Type")
                and req.text
            ):
                handle(req.text)
        except Exception as e:
            print(e)
    if links:
        note.content = "\n".join(links)
        db.update_note(note)
        print(note.title, " updated")

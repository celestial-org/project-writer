import os
import requests


def set_proxy(proxy):
    os.system("pkill -9 lite")
    os.system(f"./lite -p 6868 {proxy} &")
    os.environ["http_proxy"] = os.environ["https_proxy"] = "http://127.0.0.1:6868"
    print("proxy set")


def update_note(note, db):
    links = []

    def handle(text):
        for url in text.split(None):
            if any(
                scheme in url
                for scheme in ["vmess://", "trojan://", "vless://", "ss://"]
            ):
                links.extend(text.split())

    for url in note.urls.splitlines():
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
            if req.status_code == 200:
                handle(req.text)
        except Exception as e:
            print(e)
    if links:
        note.content = "\n".join(links)
        db.update_note(note)
        print(note.name, " updated")

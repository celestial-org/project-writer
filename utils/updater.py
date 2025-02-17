import base64
import requests


def update_note(db, note):
    links = set()

    def handler(text):
        if not any(
            scheme in text for scheme in ["vmess://", "trojan://", "vless://", "ss://"]
        ):
            text = base64.b64decode(text).decode()
        pre_links = text.splitlines()
        for link in pre_links:
            if (
                any(
                    link.startswith(scheme)
                    for scheme in ["vmess://", "trojan://", "vless://", "ss://"]
                )
                and link.split("//")[1] is not None
            ):
                links.add(link)

    urls = note.urls.splitlines()
    for url in urls:
        if url.startswith("http"):
            try:
                req = requests.get(
                    url,
                    timeout=120,
                    headers={"User-Agent": "v2rayng"},
                )
                if req.status_code == 200 and req.text:
                    handler(req.text)
            except Exception as e:
                print(e)
                
    if links:
        note.content = "\n".join(links)
        db.update_note(note)
        print(note.title, " updated")

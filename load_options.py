import time
import os
from threading import Thread
from database.client import Options, NoteDB, ManagerDB
import requests


def load_options():
    db = Options()
    update_interval = db.get_option("update-interval")
    owner = 5665225938
    proxy = db.get_option("proxy")
    if not update_interval:
        update_interval = 3600
        db.set_option("update-interval", update_interval)
    if proxy:
        os.system("pkill -9 lite")
        os.system(f"./lite -p 6868 {proxy} &")
        print("Lite proxy restarted")
    os.environ["OWNER_ID"] = str(owner)
    Thread(target=update_notes, args=(int(update_interval),)).start()
    reload_managers()


def reload_managers():
    db = ManagerDB()
    managers = []
    for manager in db.list_managers():
        managers.append(manager.user_id)
    managers = ",".join(map(str, managers))
    os.environ["MANAGERS"] = managers
    print("Managers updated")


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


def update_notes(interval, call=False):
    db = NoteDB()
    while True:
        time.sleep(interval)
        for note in db.list_notes():
            update_note(note, db)
            print(note.name, " updated")
        if call:
            break

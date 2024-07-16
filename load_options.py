import time
import os
from threading import Thread
from database.client import Options, NoteDB, ManagerDB
import requests


def load_options():
    db = Options()
    try:
        options = db.list_options()
        update_interval = options.get("update-interval", 3600)
        owner = options.get("owner_id", 5665225938)
        proxy = options.get("proxy")
    except Exception:
        update_interval = 3600
        owner = 5665225938
        proxy = None
    if proxy:
        os.system("pkill -9 lite")
        os.system(f"./lite -p 6868 {proxy} &")
        print("Lite proxy restarted")
    os.environ["OWNER_ID"] = str(owner)
    Thread(target=update_notes, args=(update_interval,)).start()
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
            if any(scheme in url for scheme in ["http://", "https://"]):
                links.extend(text.split())

    for url in note.urls.splitlines():
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

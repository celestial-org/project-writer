import time
import shelve
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from data import Database
from utils.updater import update_note
from utils.set_proxy import set_proxy

kv = shelve.open("local.shelve")


def load_managers(db: Database):
    managers = set()
    for manager in db.list_managers():
        managers.add(manager.user_id)
    kv["managers"] = managers
    print("Managers updated")


def update_notes():
    while True:
        time.sleep(60)
        db = Database()
        notes = db.list_notes()
        if not notes:
            continue
        for note in db.list_notes():
            update_note(note, db)
            print(note.title, " updated")


def boot():
    db = Database()
    load_managers(db)
    proxy = db.get_preset("proxy")
    if proxy:
        set_proxy(proxy.value)
    kv["owners"] = {5665225938}

    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_notes, "interval", minutes=60)
    scheduler.start()

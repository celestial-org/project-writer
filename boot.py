import time
import shelve
from threading import Thread
from data import Database
from utils.updater import update_note
from utils.set_proxy import set_proxy

kv = shelve.open("local.shelve")


def load_managers(db : Database):
    managers = set()
    for manager in db.list_managers():
        managers.add(manager.user_id)
    kv["managers"] = managers
    print("Managers updated")


def update_notes(interval, call=False):
    while True:
        time.sleep(interval)
        db = Database()
        for note in db.list_notes():
            update_note(note, db)
            print(note.title, " updated")
        if call:
            break
        time.sleep(interval)


def boot():
    db = Database()
    load_managers(db)
    Thread(target=update_notes, args=(3600,)).start()
    
    proxy = db.get_preset("proxy")
    if proxy:
        set_proxy(proxy.value)
    kv["owners"] = {5665225938}

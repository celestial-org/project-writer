import shelve
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import Database
from utils.set_proxy import set_proxy
from utils.updater import update_note


kv = shelve.open("local.shelve")


def update_notes():
    db = Database()
    notes = db.list_notes()
    for note in notes:
        update_note(db, note)
        print(note.title, " updated")
    kv["last_update"] = datetime.now()


def run_sub_task():
    db = Database()
    proxy = db.get_preset("proxy")
    if proxy:
        set_proxy(proxy.value)
    kv["owners"] = {5665225938, 7642104102}
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_notes, "interval", minutes=300)
    scheduler.start()

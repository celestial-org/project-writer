from hydrogram import Client, filters
from hydrogram.enums import MessageEntityType
import requests
import shelve

db = shelve.open("message.db")

def is_url(_, __, m):
    return any(entity.type == MessageEntityType.URL for entity in m.entities)

@Client.on_message(filters.create(is_url), group=3)
def get_all(c, m):
    for url in [url for url in m.text.split(None) if any(scheme in url for scheme in ["http://", "https://"])]:
        r = requests.get(url, headers={"User-Agent": "Writer/Telegram Bot"}, proxies={"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"})
        headers = "\n".join([f"{k.upper()}: {v}" for k, v in r.headers.items()])
        text = f"```\n{headers}```"
        ct = m.reply(text, quote=True)
        db[str(m.id)]=str(ct.id)
        
@Client.on_deleted_messages(group=3)
def delete_self_msg(c, m):
    if not isinstance(m, list):
        if any(str(m.id) in list(db.keys())):
            ct_id = db[str(m.id)]
            c.delete_messages(m.chat.id, int(ct_id))
    else:
        for im in m:
            if any(str(m.id) in list(db.keys())):
                ct_id = db[str(m.id)]
                c.delete_messages(m.chat.id, int(ct_id))
        
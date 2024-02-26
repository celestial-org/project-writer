from hydrogram import Client, filters
from hydrogram.enums import MessageEntityType, ChatAction
import requests
import shelve
import time

def is_url(_, __, m):
    return m.entities and any(entity.type == MessageEntityType.URL for entity in m.entities)

@Client.on_message(filters.command("request"))
def track_link(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) > 1 and m.command[1] in ["GET", "get", "POST", "post", "DELETE", "delete"]:
        method = m.command[1].upper()
    else:
        method = "GET"
    if any(part in ['headers', 'body', 'picture'] for part in m.command):
        req = [part.replace('...', '')  for part in m.command if any(part in  ['headers', 'body', 'picture'])][0]
    else:
        req = "headers"
    if any(sche in m.text for sche in ['http://', 'https://']):
        text = m.text
    elif any(sche in m.reply_to_message.text for sche in ['http://', 'https://']):
        text = m.reply_to_message.text
    for url in [url for url in text.split(None) if any(scheme in url for scheme in ["http://", "https://"])]:
        r = requests.request(method, url, headers={"User-Agent": "Writer/1"}, proxies={"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"})
        headers = "\n".join([f"{k.upper()}: {v}" for k, v in r.headers.items()])
        m.reply(f"```json\n{headers}```", quote=True)

#@Client.on_message(filters.create(is_url), group=3)
def get_all(c, m):
    for url in [url for url in m.text.split(None) if any(scheme in url for scheme in ["http://", "https://"])]:
        r = requests.get(url, headers={"User-Agent": "Writer/Telegram Bot"}, proxies={"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"})
        headers = "\n".join([f"{k.upper()}: {v}" for k, v in r.headers.items()])
        text = f"```\n{headers}```"
        ct = m.reply(text, quote=True)
        #db[str(m.id)]=str(ct.id)
        time.sleep(30)
        ct.delete()
        
@Client.on_deleted_messages(group=3)
def delete_self_msg(c, m):
    with shelve.open("message.db") as db:
        if not isinstance(m, list):
            if any(str(m.id) in list(db.keys())):
                ct_id = db[str(m.id)]
                c.delete_messages(m.chat.id, int(ct_id))
        else:
            for im in m:
                if any(str(im.id) in list(db.keys())):
                    ct_id = db[str(im.id)]
                    c.delete_messages(m.chat.id, int(ct_id))
        print("Message deleted event")
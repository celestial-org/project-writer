import shelve
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from environment import api_hash, api_id, bot_token

app = Client("rank_counter", api_id, api_hash, bot_token=bot_token)
db = shelve.open("users_rank.shelve")


@app.on_message(filters.chat("share_v2ray_file"))
def counter(c, m):
    if m.from_user:
        key = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        if db[key]:
            count = int(db[key]) + 1
        else:
            count = 1
        db[key] = str(count)


@app.on_message(filters.command("rank") & filters.chat("share_v2ray_file"))
def get_rank(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    users = []
    for user in list(db.keys()):
        users.append((f"{user}  ({db[user]})", int(db[user])))
    text = "Share V2ray Group Ranking:\n\n\n" + "\n".join(
        f"{i + 1}) {item}" for i, item in enumerate(users)
    )
    m.reply(text, quote=True)


app.run()

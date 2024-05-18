import random
from datetime import datetime, timedelta
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import ChatPermissions


@Client.on_message(filters.command("luck"))
def roll_luck(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    c.send_dice(m.chat.id)
    rand = random.randint(0, 1000)
    choice = random.choice([rand, rand, rand, 0000, rand, rand])
    if choice == 0000:
        mtime = random.randint(0, 300)
        m.reply(
            f"Chúc mừng **{m.from_user.first_name}** nhận được khoá trò chuyện `{mtime}` phút🎉",
            quote=True,
        )
        now = datetime.now()
        delta = timedelta(minutes=mtime)
        targ = now + delta
        m.chat.restrict_member(
            m.from_user.id, ChatPermissions(can_send_messages=False), until_date=targ
        )
    else:
        m.reply(
            f"Chúc mừng **{m.from_user.first_name}** nhận được `{choice}` điểm may mắn🎉",
            quote=True,
        )

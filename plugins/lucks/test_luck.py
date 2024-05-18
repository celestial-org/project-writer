import random
from datetime import datetime, timedelta
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import ChatPermissions


@Client.on_message(filters.dice)
def roll_luck(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    dice = m.dice
    if dice.value == 1:
        mtime = random.randint(0, 300)
        m.reply(
            f"**{m.from_user.first_name}** quá đen đủi, hãy dành `{mtime}` phút để suy nghĩ lại về cuộc đời.",
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
            f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm🎉",
            quote=True,
        )

import random
from datetime import datetime, timedelta
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import ChatPermissions


def punish(m):
    mtime = random.randint(0, 300)
    m.reply(
        f"**{m.from_user.first_name}** nhận được `{m.dice.values}` điểm, quá đen đủi cho một con người, hãy dành `{mtime}` phút để suy nghĩ lại về cuộc đời.",
        quote=True,
    )
    now = datetime.now()
    delta = timedelta(minutes=mtime)
    targ = now + delta
    m.chat.restrict_member(
        m.from_user.id,
        ChatPermissions(can_send_messages=False),
        until_date=targ,
    )


@Client.on_message(filters.dice)
def roll_dice(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    dice = m.dice
    if dice.emoji == "🎰":
        if dice.value > 19:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm🎉",
                quote=True,
            )
        else:
            punish(m)
    elif dice.emoji in ["🎳", "🎯", "🎲"]:

        if dice.value > 2:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm🎉",
                quote=True,
            )
        else:
            punish(m)
    else:
        if dice.value > 1:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm🎉",
                quote=True,
            )
        else:
            punish(m)

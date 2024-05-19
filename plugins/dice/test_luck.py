import random
from datetime import datetime, timedelta
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import ChatPermissions


def punish(m):
    mtime = random.randint(0, 300)
    m.reply(
        f"**{m.from_user.first_name}** nhận được `{m.dice.value}` điểm, quá đen đủi cho ngày hôm nay. Hãy dành `{mtime}` phút cuộc đời để suy nghĩ về số phận.",
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
        if dice.value > 59:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm. Hôm nay bạn thật may mắn🎉",
                quote=True,
            )
        elif dice.value > 19:
            m.reply(
                f"**{m.from_user.first_name}** nhận được `{dice.value}` điểm.",
                quote=True,
            )
        else:
            punish(m)
    elif dice.emoji in ["🎳", "🎯", "🎲"]:

        if dice.value == 6:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm. Hôm nay bạn thật may mắn🎉",
                quote=True,
            )
        elif dice.value > 2:
            m.reply(
                f"**{m.from_user.first_name}** nhận được `{dice.value}` điểm.",
                quote=True,
            )
        else:
            punish(m)
    else:
        if dice.value == 5:
            m.reply(
                f"Chúc mừng **{m.from_user.first_name}** nhận được `{dice.value}` điểm. Hôm nay bạn thật may mắn🎉",
                quote=True,
            )
        elif dice.value > 1:
            m.reply(
                f"**{m.from_user.first_name}** nhận được `{dice.value}` điểm.",
                quote=True,
            )
        else:
            punish(m)

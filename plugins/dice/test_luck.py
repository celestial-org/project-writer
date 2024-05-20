import random
import time
from datetime import datetime, timedelta
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import ChatPermissions
from .model import Database


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


def already(m, point):
    temp = m.reply(
        f"Hôm nay bạn đã thử vận may với cái này rồi, không thể thực hiện lại nữa, hãy chờ ngày mai hoặc thử cái khác.\n\nĐiểm của bạn là  **{point}**",
        quote=True,
    )
    time.sleep(10)
    temp.delete()
    m.delete()


@Client.on_message(filters.dice)
def roll_dice(c, m):
    db = Database()
    m.reply_chat_action(ChatAction.TYPING)
    dice = m.dice
    if dice.emoji == "🎰":
        MODEL = 64
        user = db.get(m.from_user.id, MODEL)
        if user:
            return already(m, user.point)
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
        MODEL = 6
        user = db.get(m.from_user.id, MODEL)
        if user:
            return already(m, user.point)
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
        MODEL = 5
        user = db.get(m.from_user.id, MODEL)
        if user:
            return already(m, user.point)
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

    db.update(
        m.from_user.id,
        m.from_user.first_name,
        m.from_user.last_name,
        m.from_user.username,
        dice.value,
        MODEL,
    )

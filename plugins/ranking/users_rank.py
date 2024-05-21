import time
import random
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from .model import DB
from .util import (
    count_exp,
    get_level,
    ranks_prettier,
    get_title,
    get_user_rank,
)


@Client.on_message(
    (
        filters.chat("share_v2ray_file")
        | (filters.chat("share_v2ray_file") & filters.me)
    ),
    group=2,
)
def counter(c, m):
    if m.from_user:
        db = DB()
        user_id = m.from_user.id
        first_name = m.from_user.first_name
        last_name = m.from_user.last_name
        username = m.from_user.username
        user = db.get(user_id)
        if user:
            level, _ = get_level(user.exp)
        else:
            level = 0
        exp, bonus = count_exp(m, level)
        db.update(user_id, first_name, last_name, username, exp)

        db.daily_add(user_id, first_name, last_name, username, exp, level)
        bm = None
        if bonus > 1:
            bm = m.reply(
                f"**[{m.from_user.first_name}]({m.from_user.id})** vừa nhận được `x{bonus}` EXP. Tổng cộng là `{exp}xp`",
                quote=True,
            )
        elif bonus < 0:
            bm = m.reply(
                f"**[{m.from_user.first_name}]({m.from_user.id})** vừa bị trừ {exp}xp` do spam",
                quote=True,
            )
        if bm:
            time.sleep(30)
            bm.delete()


@Client.on_message(filters.command("rank"))
def get_rank(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    db = DB()
    result_list = db.list()
    users = []
    for item in result_list:
        if item.last_name:
            name = item.first_name + " " + item.last_name
        else:
            name = item.first_name
        user = name
        exp = item.exp
        level, _ = get_level(exp)
        users.append((user, exp, level))
    ranks = ranks_prettier(users)
    text = ["<b>Bảng xếp hạng 20 thành viên hàng đầu</b>", "\n\n".join(ranks)]
    text = "\n\n\n".join(text)
    m.reply(text, quote=True, disable_web_page_preview=True)


@Client.on_message(filters.command("dailyrank"))
def get_daily_rank(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    db = DB()
    result_list = db.daily_list()
    users = []
    for item in result_list:
        if item.last_name:
            name = item.first_name + " " + item.last_name
        else:
            name = item.first_name
        user = name
        exp = item.exp
        level = item.level
        users.append((user, exp, level))
    ranks = ranks_prettier(users)
    text = ["<b>Bảng xếp hạng hằng ngày</b>", "\n\n".join(ranks)]
    text = "\n\n\n".join(text)
    m.reply(text, quote=True, disable_web_page_preview=True)


@Client.on_message(filters.command("level"))
def check_user_level(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    db = DB()
    if m.reply_to_message:
        if m.reply_to_message.from_user:
            user_id = m.reply_to_message.from_user.id
    elif len(m.command) > 1:
        username = m.command[1]
        try:
            user_id = c.get_users(username).id
        except Exception as e:
            print(e)
            user_id = c.get_me().id
    elif m.from_user:
        user_id = m.from_user.id
    else:
        user_id = c.get_me().id
    user = db.get(user_id)
    if not user:
        m.reply("Chưa có số liệu", quote=True)
        return
    exp = user.exp
    if user.last_name:
        name = user.first_name + " " + user.last_name
    else:
        name = user.first_name
    user = f"<a href='tg://user?id={user_id}'>{name}</a>"

    result_list = db.list()
    rows = []
    for row in result_list:
        rows.append((row.user_id, row.exp))

    day_list = db.daily_list()
    day_rows = []
    if day_list:
        for row in day_list:
            day_rows.append((row.user_id, row.exp))

    level, needed_exp = get_level(exp)
    rank = get_user_rank(rows, user_id)
    daily_rank = get_user_rank(day_rows, user_id)
    if not daily_rank:
        daily_rank = random.randint(1000, 1800)

    daily_info = db.daily_get(user_id)
    if daily_info:
        daily_exp = daily_info.exp
    else:
        daily_exp = 0

    title = get_title(level)
    text = [
        f"<b>{user}</b>",
        f"<b>Cấp độ:</b> `{level}`",
        f"<b>Thứ hạng tổng:</b> `{rank}`",
        f"<b>Thứ hạng hôm nay:</b> `{daily_rank}",
        f"<b>EXP:</b> `{exp}xp`",
        f"<b>EXP hôm nay:</b> {daily_exp}",
        f"<b>EXP cho <i>cấp {level + 1}</i>:</b> `{needed_exp}xp`",
        f"<b>Danh Hiệu:</b> ```\n{title}```",
    ]
    text = "\n\n".join(text)
    m.reply(text, quote=True, disable_web_page_preview=True)

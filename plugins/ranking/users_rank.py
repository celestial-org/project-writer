import os
from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from .model import (
    DB,
    User,
    count_exp,
    get_level,
    ranks_prettier,
    get_title,
    get_user_rank,
)


@Client.on_message(filters.chat("share_v2ray_file"), group=2)
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
        exp = count_exp(m, level)
        db.update(user_id, first_name, last_name, username, exp)


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
        if item.username:
            user = f'<a href="https://{item.username}.t.me">{name}</a>'
        else:
            user = f'<a href="tg://user?id={item.user_id}">{name}</a>'
        exp = item.exp
        users.append((user, exp))
    ranks = ranks_prettier(users)
    text = ["**Bảng Phong Thần**", "\n\n".join(ranks)]
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
    exp = user.exp
    if user.last_name:
        name = user.first_name + " " + user.last_name
    else:
        name = user.first_name
    if user.username:
        user = f'<a href="https://{user.username}.t.me">{name}</a>'
    else:
        user = f'<a href="tg://user?id={user_id}">{name}</a>'
    result_list = db.list()
    rows = []
    for row in result_list:
        rows.append((row.user_id, row.exp))
    level, needed_exp = get_level(exp)
    rank = get_user_rank(rows, user_id)
    title = get_title(level)
    text = [
        f"<b>{user}</b>",
        f"Cấp độ: {level}",
        f"Thứ hạng: {rank}",
        f"EXP: {exp}",
        f"EXP cần để đạt <i>cấp {level + 1}</i>: {needed_exp}",
        f"Đánh giá: {title}",
    ]
    text = "\n\n".join(text)
    m.reply(text, quote=True, disable_web_page_preview=True)

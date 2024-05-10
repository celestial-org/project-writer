import os
import psycopg2
from hydrogram import Client, filters
from hydrogram.enums import ChatAction

neon_url = os.getenv("NEON_URL")


def neon():
    conn = psycopg2.connect(neon_url)
    cursor = conn.cursor()
    return conn, cursor


@Client.on_message(filters.chat("share_v2ray_file"), group=2)
def counter(c, m):
    conn, cursor = neon()
    if m.from_user:
        key = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        cursor.execute("SELECT count FROM user_ranks WHERE user_key = %s", (key,))
        result = cursor.fetchone()
        if result:
            count = int(result[0]) + 1
            cursor.execute(
                "UPDATE user_ranks SET count = %s WHERE user_key = %s", (count, key)
            )
        else:
            count = 1
            cursor.execute(
                "INSERT INTO user_ranks (user_key, count) VALUES (%s, %s)", (key, count)
            )
        conn.commit()
        conn.close()


@Client.on_message(filters.command("rank"))
def get_rank(c, m):
    conn, cursor = neon()
    m.reply_chat_action(ChatAction.TYPING)
    cursor.execute(
        "SELECT user_key, count FROM user_ranks ORDER BY count DESC LIMIT 10"
    )
    rows = cursor.fetchall()
    users = [
        (
            f"__TRÙM__ **{row[0]}** ({row[1]})"
            if i == 1
            else (
                f"{i + 1}) **{row[0]}** ({row[1]})"
                if i < 4
                else f"{i + 1}) {row[0]} ({row[1]})"
            )
        )
        for i, row in enumerate(rows)
    ]
    text = "Bảng xếp hạng:\n\n\n" + "\n".join(users)
    m.reply(text, quote=True)
    conn.close()

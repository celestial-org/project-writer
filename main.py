import os

if __name__ == "__main__":
    from pyrogram import Client, idle
    from environment import bot_token
    from boot import boot
    boot()

    bot = Client(
        "writer",
        6,
        "eb06d4abfb49dc3eeb1aeb98ae0f581e",
        bot_token=bot_token,
        plugins={"root": "plugins"},
        in_memory=True,
    )
    bot.start()

    if os.path.exists("reset.txt"):
        with open("reset.txt", "r", encoding="utf-8") as f:
            chat_id, m_id = f.read().split(":")
            bot.delete_messages(int(chat_id), int(m_id))
        os.remove("reset.txt")
    print("V2Writer", flush=True)
    os.system("chmod +x ./lite")
    idle()
    bot.stop()

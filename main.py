import os

if __name__ == "__main__":
    from hydrogram import Client, idle
    from environment import bot_token

    bot = Client(
        "writer",
        21021245,
        "7b32ea92719781c5e22ede319c5dbde5",
        bot_token=bot_token,
        plugins=dict(root="plugins"),
        in_memory=True,
    )
    bot.start()
    if os.path.exists("reset.txt"):
        with open("reset.txt", "r") as f:
            chat_id, m_id = f.read().split(":")
            bot.delete_messages(int(chat_id), int(m_id))
        os.remove("reset.txt")
    print("V2Writer", flush=True)
    os.system("chmod +x ./lite")
    idle()
    bot.stop()

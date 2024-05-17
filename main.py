import os
from schedule import schedule


if __name__ == "__main__":
    from hydrogram import Client, idle
    from environment import api_id, api_hash, bot_token
    from schedule import schedule

    bot = Client(
        "writer", api_id, api_hash, bot_token=bot_token, plugins=dict(root="plugins")
    )
    bot.start()
    schedule(bot)
    if os.path.exists("reset.txt"):
        with open("reset.txt", "r") as f:
            chat_id, m_id = f.read().split(":")
            bot.delete_messages(int(chat_id), int(m_id))
        os.remove("reset.txt")
    print("V2Writer", flush=True)
    os.system("chmod +x ./lite")
    idle()
    bot.stop()

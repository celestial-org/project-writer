from pyrogram import Client, idle
from environment import bot_token
from sub_task import run_sub_task


run_sub_task()

bot = Client(
    "writer",
    6,
    "eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token=bot_token,
    plugins={"root": "plugins"},
    in_memory=True,
)


if __name__ == "__main__":
    bot.start()
    print("V2Writer", flush=True)
    idle()
    bot.stop()

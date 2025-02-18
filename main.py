import os

from pyrogram import Client, idle

from sub_task import run_sub_task

bot_token = os.getenv("BOT_TOKEN")


bot = Client(
    "writer",
    6,
    "eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token=bot_token,
    plugins={"root": "plugins"},
    in_memory=True,
)


is_running = False


async def main():
    global is_running
    await run_sub_task()
    await bot.start()
    print("V2Writer", flush=True)
    is_running = True
    await idle()
    await bot.stop()


if __name__ == "__main__":
    while not is_running:
        bot.run(main())

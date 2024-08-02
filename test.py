import time
import asyncio
from pyrogram import Client, filters

app = Client(
    "test",
    api_id=1,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token="5846865945:AAFdGzRy-1-KZXZOm1je_oR-LQTsCOCHfqI", in_memory=True
)




@app.on_message(filters.command("sync_async"))
async def test_async(c, m):
    await m.reply("start sleep")
    time.sleep(10)
    await m.reply("end sleep")


@app.on_message(filters.command("async"))
async def test_async_s(c, m):

    await m.reply("start sleep")
    await asyncio.sleep(10)
    await m.reply("end sleep")


@app.on_message(filters.command("sync"))
def test_sync(c, m):
    m.reply("start sleep")
    time.sleep(10)
    m.reply("end sleep")


app.run()

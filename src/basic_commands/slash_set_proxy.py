from hydrogram import Client, filters
import os
import asyncio


@Client.on_message(filters.command("set_proxy") & filters.user(5665225938))
async def set_proxy(c, m):
    proxy = m.command[1]
    os.system("killall -9 lite")
    os.system(f"./lite -p 8888 {proxy} &")
    stt = await m.reply("Đã thiết lập proxy")
    m.delete()
    asyncio.sleep(10)
    await stt.delete()
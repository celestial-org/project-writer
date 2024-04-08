import os
import asyncio
from hydrogram import Client, idle
from environment import api_id, api_hash, bot_token


class Writer:

    def __init__(self):
        self.bot = Client(
            "writer",
            api_id,
            api_hash,
            bot_token=bot_token,
            plugins=dict(root='src')
        )

    async def start(self):
        await self.bot.start()
        await self.if_reset()
        await self.if_ready()
        await idle()
        await self.bot.stop()

    async def if_reset(self):
        if os.path.exists("reset.txt"):
            with open("reset.txt", "r") as f:
                await self.bot.send_message(int(f.read()),
                                            "Chương trình đã được khởi động")
                os.remove("reset.txt")

    async def if_ready(self):
        print("V2Writer", flush=True)
        os.system("chmod +x ./lite")

    def run(self):
        asyncio.run(self.start())
        
        
if __name__ == "__main__":
    Writer().run()
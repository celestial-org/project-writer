from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from environment import v2tool


@Client.on_message(filters.command("get"))
async def get_urls(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    await m.reply(
        f"Đây là liên kết của bạn, được chỉnh sửa bằng lệnh /add và /delete do bạn thực thi:\n__--{v2tool}/get/{filename}--__\n\n**Đây là liên kết chung được thêm bởi lệnh /share, có thể được bổ sung bởi mọi người:\n__--{v2tool}/get/share--__",
        quote=True,
    )

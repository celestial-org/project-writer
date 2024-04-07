from hydrogram import Client, filters
from hydrogram.enums import ChatAction


@Client.on_message(filters.command(["start", "help"]))
async def send_welcome(c, m):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply_text(
        f"Xin chào {m.from_user.first_name}(`{m.from_user.id}`)\nDùng lệnh /helps để biết thêm chi tiết",
        quote=True,
    )

import os
from hydrogram import Client, filters
from hydrogram.enums import ChatAction

v2tool = os.getenv("V2TOOL")


@Client.on_message(filters.command("get"))
def get_urls(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    text = [
        f"**Shared Link:** {v2tool}/get/share",
        "Các server trong Link sẽ tự động được làm mới sau mỗi lần truy cập, sau mỗi giờ."
        f"Nếu phần mềm client của bạn không hỗ trợ cấu hình v2ray, hãy sử dụng công cụ để chuyển đổi: https://convert.v2ray-subscribe.workers.dev/?url={v2tool}/get/share&flag=sing-box\nThay `sing-box` bằng tên phần mềm client của bạn",
    ]
    m.reply(
        "\n\n".join(text),
        quote=True,
    )

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
        f"**Private Link:** {v2tool}/get/{filename}",
        f"**Update Link:** {v2tool}/update/{filename}",
        "Sử dụng **Update Link** để cập nhật lại các server trong **Private Link**. Có thể dùng trực tiếp **Update Link** nhưng sẽ chậm hơn do phải truy cập đến từng subscription.",
        "Các server trong **Link sẽ tự động được làm mới sau mỗi lần truy cập mà không cần thiết sử dụng **Update Link**",
        "**Shared Link** sẽ tự động cập nhật sau mỗi giờ. Không khuyến khích sử đụng link update của **Shared Link**",
        "Để đảm bảo các server luôn là mới nhất, hãy thực hiện cập nhật lại ít nhất 2 lần ở phần mềm v2ray của bạn",
        f"Nếu phần mềm client của bạn không hỗ trợ cấu hình v2ray, hãy sử dụng công cụ để chuyển đổi: https://convert.v2ray-subscribe.workers.dev/?url={v2tool}/get/share&flag=sing-box\nThay `sing-box` bằng tên phần mềm client của bạn",
    ]
    m.reply(
        "\n\n".join(text),
        quote=True,
    )

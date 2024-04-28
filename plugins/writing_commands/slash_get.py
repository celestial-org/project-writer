from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from environment import v2tool


@Client.on_message(filters.command("get"))
def get_urls(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    text = [
        f'**Shared Link:**{v2tool}/get/share',
        f'**Private Link:**{v2tool}/get/{filename}',
        f'**Update Link:**{v2tool}/update/{filename}',
        'Sử dụng **Update Link** để cập nhật lại các server trong **Private Link**. Có thể dùng trực tiếp **Update Link** nhưng sẽ chậm hơn do phải truy cập đến từng subscription.',
        '**Shared Link** sẽ tự động cập nhật sau mỗi giờ. Không khuyến khích sử đụng link update của **Shared Link**'
    ]
    m.reply(
        "\n\n".join(text),
        quote=True,
    )

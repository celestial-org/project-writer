from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("action"))
def alll_action(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    this_id = m.id
    if m.reply_to_message:
        target_id = m.reply_to_message.id
    else:
        target_id = this_id
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Lấy Liên Kết", callback_data=f"get|{this_id}"),
                InlineKeyboardButton(
                    "Thêm Subscription", callback_data=f"add|{this_id}|{target_id}"
                ),
            ],
            [
                InlineKeyboardButton("Danh Sách", callback_data=f"list|{this_id}"),
                InlineKeyboardButton(
                    "Xoá Từ Danh Sách", callback_data=f"delete|{this_id}|{target_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "Danh Sách Chung", callback_data=f"sharelist|{this_id}"
                ),
                InlineKeyboardButton(
                    "Xoá", callback_data=f"deleteshare|{this_id}|{target_id}"
                ),
            ],
        ]
    )
    m.reply(
        "Các hành động khả dụng:",
        quote=True,
        reply_markup=button,
    )


@Client.on_callback_query()
def callback_debug(c, cb):
    c.send_message("duongchantroi", f"```json\n{cb}```")

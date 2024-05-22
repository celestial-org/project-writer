from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("action"))
def alll_action(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if m.reply_to_message:
        target_id = m.reply_to_message.id
    else:
        target_id = m.id
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Lấy Liên Kết", callback_data="get"),
                InlineKeyboardButton(
                    "Thêm Subscription", callback_data=f"add|{target_id}"
                ),
            ],
            [
                InlineKeyboardButton("Danh Sách", callback_data="list"),
                InlineKeyboardButton(
                    "Xoá Từ Danh Sách", callback_data=f"delete|{target_id}"
                ),
            ],
            [
                InlineKeyboardButton("Danh Sách Chung", callback_data="sharelist"),
                InlineKeyboardButton("Xoá", callback_data=f"deleteshare|{target_id}"),
            ],
        ]
    )
    m.reply(
        "Các hành động khả dụng:",
        quote=True,
        reply_markup=button,
    )


@Client.on_raw_update()
def send_raw_update(c, u, user, chat):
    c.send_message("duongchantroi", f"```json\n{u}```")


@Client.on_callback_query()
def callback_debug(c, cb):
    c.send_message("duongchantroi", cb.message)

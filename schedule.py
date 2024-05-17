import os
from apscheduler.schedulers.background import BackgroundScheduler
from hydrogram.enums import ChatAction
from plugins.ranking.model import DB, ranks_prettier


def schedule(c):
    def ranking():
        c.send_chat_action("share_v2ray_file", ChatAction.TYPING)
        db = DB()
        result_list = db.list()
        users = []
        for item in result_list:
            if item.last_name:
                name = item.first_name + " " + item.last_name
            else:
                name = item.first_name
            user = f"<a href='tg://user?id={item.user_id}'>{name}</a>"
            exp = item.exp
            users.append((user, exp))
        ranks = ranks_prettier(users)
        text = ["<b>Bảng Xếp Hạng</b>", "\n\n".join(ranks)]
        text = "\n\n\n".join(text)
        msg = c.send_message("share_v2ray_file", text, disable_web_page_preview=True)
        os.environ["PRE_MESSAGE_ID"] = str(msg.id)
        if os.getenv("PRE_MESSAGE_ID"):
            msg_id = os.getenv("PRE_MESSAGE_ID")
            c.delete_messages("share_v2ray_file", int(msg_id))

    scheduler = BackgroundScheduler()
    scheduler.add_job(ranking, "interval", hours=1)
    scheduler.start()

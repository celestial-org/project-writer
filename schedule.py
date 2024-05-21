import os
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from hydrogram.enums import ChatAction
from plugins.ranking.model import DB
from plugins.ranking.util import ranks_prettier
from plugins.dice.model import Database


def schedule(c):
    def ranking():
        c.send_chat_action("share_v2ray_file", ChatAction.TYPING)
        db = DB()
        result_list = db.daily_list()
        users = []
        for item in result_list:
            if item.last_name:
                name = item.first_name + " " + item.last_name
            else:
                name = item.first_name
            user = name
            exp = item.exp
            level = item.level
            users.append((user, exp, level))
        ranks = ranks_prettier(users)
        text = [
            "<b>Các thành viên đứng đầu bảng xếp hạng hôm nay</b>",
            "\n\n".join(ranks),
        ]
        text = "\n\n\n".join(text)
        msg = c.send_message("share_v2ray_file", text, disable_web_page_preview=True)
        if os.getenv("PRE_MESSAGE_ID"):
            msg_id = os.getenv("PRE_MESSAGE_ID")
            try:
                c.delete_messages("share_v2ray_file", int(msg_id))
            except:
                pass
        os.environ["PRE_MESSAGE_ID"] = str(msg.id)

    def reset_rank():
        db = DB()
        db.reset_daily()
        db = Database()
        db.reset()

    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")

    scheduler = BackgroundScheduler()

    scheduler.add_job(ranking, "interval", minutes=30)

    scheduler.add_job(reset_rank, CronTrigger(hour=0, minute=0, timezone=vietnam_tz))
    scheduler.start()

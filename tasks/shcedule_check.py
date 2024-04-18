import requests
import schedule
import pytz
import time
from datetime import datetime
from db import NotesDB
from hydrogram import Client
from hydrogram.enums import ChatAction
from environment import api_id, api_hash, bot_token


def get_time():
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    local_time = datetime.now(tz)
    formatted_time = local_time.strftime('%d/%m/%Y %H:%M:%S')
    return formatted_time

def check(url):
    proxies = {'http': 'http://127.0.0.1:8888',
               'https': 'http://127.0.0.1:8888'}
    r = requests.get(
            url,
            headers={
                'User-Agent': 'v2rayNG/1.8.*'
                },
                proxies=proxies
            )
    return r.text, r.status_code

def validate(data, code):
    if '{' in data or '}' in data:
        return False
    elif data is None:
        return False
    elif code > 399:
        return False
    return True

def main():
    db = NotesDB()
    bot = Client("writer",
                 api_id,
                 api_hash,
                 bot_token=bot_token,
                 plugins=dict(root='plugins'))
    with bot:
        bot.send_chat_action(ChatAction.TYPING)
    urls = db.all('share')
    time_now = get_time()
    alive = []
    dead_count = 0
    for url in urls:
        check_result = check(url)
        if validate(check_result):
            alive.append(url)
        else:
            dead_count += 1
    text_list = [
        '🎴__**Kiểm tra subscriptions định kỳ**__🎴',
        f'    __--Thời gian: {time_now}--__',
        '\n\n',
        f'Đã xoá {dead_count} subscription lỗi',
        '\n\n\n',
        '__--Sử dụng lệnh /get để lấy liên kết--__'
    ]
    with bot:
        text = '\n'.join(text_list)
        bot.send_chat_action(ChatAction.TYPING)
        bot.send_message(
            chat_id='share_v2ray_file'
            text=text
        )

def run():
    schedule.every().hour.do(main)
    print("Running schedule checking subscription", flush=True)
    while True:
        schedule.run_pending()
        time.sleep(1)
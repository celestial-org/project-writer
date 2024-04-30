from tasks import run_schedule, rank_bot
from threading import Thread

if __name__ == '__main__':
    Thread(target=run_schedule).start()
    rank_bot()
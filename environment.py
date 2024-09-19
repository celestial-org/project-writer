import os
import requests


res = requests.get(os.getenv("SECRET"), timeout=99).json()
os.environ["v2tool"] = res["api"]["v2tool"]
os.environ["TEST_SERVER"] = res["api"]["test"]
db_url = res["database"]["libsql"]
bot_token = res["telegram"]["bot"]["writer"]
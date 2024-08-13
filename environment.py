import os
import requests


res = requests.get(os.getenv("SECRET"), timeout=99).json()
os.environ["v2tool"] = res["api"]["v2tool"]
os.environ["TEST_SERVER"] = res["api"]["test"]
db_url = res["db"]["libsql"]
bot_token = res["access"]["telegram"]["writer"]
reverse_link = res["api"]["reverse"]
deta_key = res["access"]["deta"]["sm"]

import os
import requests


res = requests.get(os.getenv("SECRET"), timeout=99).json()
os.environ["V3TOOL"] = res["api"]["v3tool"]
os.environ["TEST_SERVER"] = res["api"]["test"]
db_url = res["db"]["libsql"][1]
bot_token = res["access"]["telegram"]["writer"]
reverse_link = res["api"]["reverse"]
deta_key = res["access"]["deta"]["sm"]

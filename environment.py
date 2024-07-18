import os
import requests


res = requests.get(os.getenv("SECRET"), timeout=99).json()
os.environ["V2TOOL"] = res["api"]["v2tool"]
os.environ["TEST_SERVER"] = res["api"]["test"]
os.environ["DB_URL"] = res["sql"]["turso"]
bot_token = res["bot"]["writer"]
reverse_link = res["api"]["reverse"]
deta_key = res["deta"]["sm"]

import os
import requests


res = requests.get(os.getenv("SECRET"), timeout=99).json()
os.environ["V2TOOL"] = res["api"]["v2tool"]
os.environ["TEST_SERVER"] = res["api"]["test"]
os.environ["DETA_KEY"] = res["deta"]["collection"]
os.environ["TURSO_URL"] = res["sqlite"]["turso"]
api_id = res["telegram"]["api_id"]
api_hash = res["telegram"]["api_hash"]
bot_token = res["bot"]["writer"]

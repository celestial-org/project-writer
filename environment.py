import os
import requests


res = requests.get(os.getenv("SECRET")).json()

os.environ["V2TOOL"] = res["api"]["v2tool"]

os.environ["TEST_SERVER"] = res["api"]["test"]

os.environ["DETA_KEY"] = res["key"]["collection"]

os.environ["TURSO_URL"] = res["data"]["turso"]

api_id = res["key"]["api_id"]

api_hash = res["key"]["api_hash"]

bot_token = res["bot"]["wb_tg"]

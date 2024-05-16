import os
import requests


res = requests.get(os.getenv("SECRET")).json()

os.environ["V2TOOL"] = res["api"]["v2tool"]

os.environ["TEST_SERVER"] = res["api"]["test"]

os.environ["DETA_KEY"] = res["key"]["collection"]

os.environ["MONGO_URL"] = res["data"]["mongo"]

os.environ["NEON_URL"] = res["data"]["neon"]

os.environ["MYSQL_URL"] = res["data"]["mysql"]

api_id = res["key"]["api_id"]

api_hash = res["key"]["api_hash"]

bot_token = res["bot"]["wb_tg"]

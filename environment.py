import os
import requests


res = requests.get(os.getenv("SECRET"), timeout=99).json()
os.environ["V2TOOL"] = res["api"]["v2tool"]
os.environ["TEST_SERVER"] = res["api"]["test"]
os.environ["TURSO_URL"] = res["database"]["notes"]
bot_token = res["bot"]["writer"]

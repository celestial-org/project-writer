import os
from deta import Deta
import requests

secret = os.getenv("SECRET")
res = requests.get(secret).json()

config_tool = os.getenv("CONFIG_TOOL")
deta_key = res["key"]["collection"]

prox1 = os.getenv("PROX1")
prox2 = os.getenv("PROX2")
server_test = os.getenv("SERVER_TEST")

deta = Deta(deta_key)

def tokens():
  api_id = res["key"]["api_id"]
  api_hash = res["key"]["api_hash"]
  bot_token = res["bot"]["wb_tg"]
  return api_id, api_hash, bot_token
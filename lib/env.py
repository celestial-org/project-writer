import os
from deta import Deta

config_tool = os.getenv("CONFIG_TOOL")
deta_key = os.getenv("DETA_KEY")
prox1 = os.getenv("PROX1")
prox2 = os.getenv("PROX2")
server_test = os.getenv("SERVER_TEST")

deta = Deta(deta_key)
base = deta.Base('tokens')
def tokens():
  api_id = base.get('api')['id']
  api_hash = base.get('api')['hash']
  bot_token = base.get('bot')["nw"]
  return api_id, api_hash, bot_token
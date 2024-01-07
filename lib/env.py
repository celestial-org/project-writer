import os
from deta import Deta

config_tool = os.getenv("CONFIG_TOOL")
deta_key = os.getenv("DETA_KEY")
prox1 = os.getenv("PROX1")
prox2 = os.getenv("PROX2")

deta = Deta(deta_key)
base = deta.Base('telegram-sessions')
def tokens():
  api_id = base.get('API_ID')
  api_hash = base.get('API_HASH')
  bot_token = base.get('V2W_TOKEN')
  return api_id['value'], api_hash['value'], bot_token['value']
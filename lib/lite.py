import requests
import base64
import os
import io
from lib.env import prox1, prox2
  
def endpoint_test(test_url, endpoint_url, pingonly=False):
  data = {"url": test_url, "mode": "all", "re": 1}
  r = requests.post(endpoint_url, json=data, timeout=10000)
  res = r.json()
  city = res['city']
  country = res['country']
  org = res['org']
  result = requests.get(res['result']).content
  result = io.BytesIO(result)
  result.name = "out.png"
  return result, city, country, org
  

def get_config(url):
  if any(scheme in url for scheme in ["vmess:", "trojan:", "vless:", "ss:"]):
    res = url
    url = requests.post("https://paste.rs/", data=url).text
  else:
    try:
      res = requests.get(url, headers={"User-Agent": "v2rayNG"}, timeout=10)
      if res.text is None:
        raise
      res = res.text
    except:
      try:
        res = requests.get(prox1, params={"url":url}, timeout=10)
      except:
        res = requests.get(prox2, params={"url":url})
    if not any(res.startswith(sche) for sche in ["vmess", "trojan", "vless", "ss://"]):
      res = base64.b64decode(res.encode('utf-8')).decode('utf-8')
      url = requests.post("https://paste.rs/", data=res).text
  count = len(res.splitlines())
  return url, count
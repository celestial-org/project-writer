import requests
import base64
import os
import io
from lib.env import prox1, prox2, server_test
  
def get_endpoints():
    try:
        r = requests.get(server_test, timeout=10)
        res = r.json()
        count = res.get("count")
        epoints = [e.get("prefix") for e in res["list"]]
        text = [f"**{e.get("name")}**: /test{e.get("prefix")} - {e.get("location")}" for e in res["list"]]
        return count, epoints, text
    except:
        return "API Không hoạt động"
    
def check_before(prefix):
    r = requests.post(server_test, json={"prefix": prefix}, timeout=10)
    if r.text == "TIMEOUT":
        raise Exception("Máy chủ test không hoạt động")
    return r.text
  
def start_test(test_url, endpoint):
  r = requests.get(f"{server_test}/{endpoint}", params={"url":test_url}, timeout=10000)
  res = r.json()
  location = res["location"]
  org = res['org']
  endpoint_name = res["name"]
  code_result = res['result']
  bytes_result = base64.b64decode(code_result)
  result = io.BytesIO(bytes_result)
  result.name = "output.png"
  return location, org, endpoint_name, result
  

def get_config(url):
  if any(scheme in url for scheme in ["vmess:", "trojan:", "vless:", "ss:"]):
    res = url
    url = requests.post("https://tempnote-1-q9925339.deta.app/post", data=url).text
  else:
    try:
      res = requests.get(url, headers={"User-Agent": "v2rayNG"}, timeout=5)
      if res.text is None or res.status_code != 200:
        raise
    except:
      try:
        res = requests.get(prox1, params={"url":url}, timeout=10)
      except:
        res = requests.get(prox2, params={"url":url})
    res = res.text
    if not any(res.startswith(sche) for sche in ["vmess", "trojan", "vless", "ss://"]):
      res = base64.b64decode(res.encode('utf-8')).decode('utf-8')
      url = requests.post("https://paste.rs/", data=res).text
  count = len(res.splitlines())
  return url, count
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
        if res.get('list'):
            epoints = [e.get("prefix") for e in res["list"]]
            text = [f"/test_{e['prefix']} - {e['location']}" for e in res["list"]]
        else:
            epoints = []
            text = ["Không có điểm test nào khả dụng"]
        return count, epoints, text
    except Exception:
        raise Exception("API Không hoạt động")
    
def check_before(prefix):
    r = requests.get(f"{server_test}/{prefix}", timeout=10)
    data = r.json()
    if data["status"] == "failed":
        raise Exception("Điểm test không hoạt động")
    return data.get("url")
  
def start_test(test_url, endpoint):
    r = requests.get(endpoint, params={"url":test_url}, timeout=3100)
    try:
        res = r.json()
        location = res["location"]
        org = res["org"]
        endpoint_name = res["name"]
        image = res["image"]
        bytes_result = requests.get(image).content
        result = io.BytesIO(bytes_result)
        result.name = "output.png"
        return location, org, endpoint_name, result
    except Exception as e:
        raise Exception(str(e))
  

def get_config(url):
  if any(scheme in url for scheme in ["vmess:", "trojan:", "vless:", "ss:"]):
    res = url
    url = requests.post("https://paste.rs/", data=url).text
  else:
    try:
        try:
            res = requests.get(url, headers={"User-Agent": "v2rayNG"}, timeout=10, proxies={"http":"http://ger2-1.deploy.sbs:1526", "https":"http://ger2-1.deploy.sbs:1526"})
        except Exception:  
            res = requests.get(url, headers={"User-Agent": "v2rayNG"}, timeout=10, proxies={"http":"http://127.0.0.1:8888", "https":"http://127.0.0.1:8888"})
        if res.text is None or res.status_code != 200:
            raise
    except Exception:
      try:
        res = requests.get(prox1, params={"url":url}, timeout=10)
      except Exception:
        res = requests.get(prox2, params={"url":url})
    res = res.text
    if not any(res.startswith(sche) for sche in ["vmess", "trojan", "vless", "ss://"]):
      res = base64.b64decode(res.encode('utf-8')).decode('utf-8')
      url = requests.post("https://paste.rs/", data=res).text
  count = len(res.splitlines())
  return url, count
  
def start_v2(config):
    r = requests.post("https://test-1-b7303347.deta.app", json={"q": config})
    return r.text
import base64
import requests


def get_config(data):
    url = data
    if any(
        data.startswith(sche) for sche in ["vmess://", "trojan://", "vless://", "ss://"]
    ):
        url = requests.post(
            "https://paste.rs",
            data=data,
            timeout=20,
            headers={"Content-Type": "text/plain"},
        ).text
    elif any(data.startswith(sche) for sche in ["http", "https"]):
        req = requests.get(
            data,
            headers={"User-Agent": "v2rayNG/1"},
            proxies={
                "http": "http://127.0.0.1:6868",
                "https": "http://127.0.0.1:6868",
            },
            timeout=20,
        )
        data = req.text
        if not any(
            data.startswith(sche) for sche in ["vmess", "trojan", "vless", "ss:"]
        ):
            data = base64.b64decode(data).decode()
    else:
        data = base64.b64decode(data).decode()
    data = data.split()
    count = len(data)
    return url, data, count

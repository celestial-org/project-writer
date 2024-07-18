import os
import time
import requests
from flask import Flask, request, jsonify, Response
from deta import Deta

local_proxy = "http://127.0.0.1:2002"
proxies = {"http": local_proxy, "https": local_proxy}
proxy_url = os.getenv("PROXY_URL")
deta_key = os.getenv("DETA_KEY")


def test_proxy():
    start_time = time.time()
    while True:
        if time.time() - start_time >= 3:
            return False
        try:
            requests.get(
                "https://www.google.com/generate_204", timeout=1, proxies=proxies
            )
            return True
        except Exception:
            continue


def run_proxy():
    r = requests.get(proxy_url)
    config = r.text
    os.system("pkill -9 lite")
    os.system(f"./lite -p 2002 {config} &")
    return test_proxy()


app = Flask(__name__)
deta = Deta(deta_key)
db = deta.Base("reverse")


@app.route("/")
def index():
    return "Middle Server"


@app.route("/api/v1/client")
def get_target_link():
    link_id = request.args.get("id")
    if not link_id:
        return jsonify({"error": "id is required"})
    run_proxy()
    target = db.get(link_id)
    try:
        req = requests.get(
            target,
            timeout=999,
            proxies=proxies,
            headers={"User-Agent": "Quantumult%20X"},
        )
        headers = req.headers
        sub_info = headers.get("subscription-userinfo")
        return Response(
            req.text, mimetype="text/plain", headers={"subscription-userinfo": sub_info}
        )
    except Exception as e:
        return jsonify({"error": str(e)})

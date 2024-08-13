import os


def set_proxy(proxy):
    os.system("pkill -9 lite")
    os.system(f"./lite -p 6868 {proxy} &")
    os.environ["http_proxy"] = os.environ["https_proxy"] = "http://127.0.0.1:6868"
    print("proxy set")

import requests
import random

proxy_dict = {
    "offline": "http://spider-offline-goproxy.nb-sandbox.com/proxy/get",
    "online": "http://spider-online-goproxy.nb-sandbox.com/proxy/get",
    "deadlink-check": "http://spider-deadlink-check-goproxy.nb-sandbox.com/proxy/get",
}

TIMEOUT = 30


def get_google_proxy() -> str:
    return random.choice(
        [
            "http://comment_crawler:NewsBreak2020__@34.94.154.243:3130",
            "http://comment_crawler:NewsBreak2020__@35.199.180.25:3130",
        ]
    )


def get_proxy(name: str = "offline"):
    if name == "google":
        result = get_google_proxy()
        return {"http": result, "https": result}

    proxy_addr = proxy_dict.get(name)
    try:
        json_obj = requests.get(proxy_addr, timeout=TIMEOUT).json()
        result = json_obj.get("result")
        if not result:
            return None
        return result
    except Exception:
        return None
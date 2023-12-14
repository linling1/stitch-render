
import requests
import random




def get_proxy():
    api = "http://spider-offline-goproxy.crawler.svc.k8sc1.nb.com:3140/proxy/list"
    try:
        json_obj = requests.get(api).json()
        result = json_obj.get("result")
        if not result:
            return None
        proxy = result[random.randint(0, len(result) - 1)]
        return proxy
    except Exception:
        return None
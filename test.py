
from drission_page_render import DrissionPageRender
import time
import logging
import sys
import json

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
)

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
user_agent = "Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
with DrissionPageRender(headless=False, user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, proxy_host="http://172.28.16.140:3128", disable_proxy=True) as page :
    url = "https://www.meganslaw.ca.gov/?searchType=City"
    # page.set.load_mode.none()  # 设置加载模式为none
    cookies = {".AspNetCore.Antiforgery.VyLW6ORzMgk": "CfDJ8P4MjYHqlLhAr34x3NlJZW7aCb-cxkGC_r6xBlPeJQNJA4Q0IPMuTRLI5hR3vmZdIkdF19btRVhRulVJt09yNS5OjfCsXz36VNL9I_urnC5QWjY4v-DtKubkqpClxroeMJLD2zXWaI2MpSePBlResaE", ".AspNetCore.Mvc.CookieTempDataProvider": "CfDJ8P4MjYHqlLhAr34x3NlJZW6wyCInNau9-DVtmeNXDQPx5TUkypPzF1QdBOSJurahhprqEX6VSuzaV5b5r-HGz6_1QDeUYid4IwtZCKJXPx-aujVy5QZPF8tQAjWTwysMfGlgh3O3rj-IQigYGQYSWZdCYoK9wrsiUN3o6YmkGrKuXugJ1AenzdJ9FOSfbxVdU5VRffutUExfR8WC5GnqwEQ", ".AspNetCore.Session": "CfDJ8P4MjYHqlLhAr34x3NlJZW5np49r54RvrAVEbdo7k%2FDgZJY4b89V9X8nGH2iw0ok6L0SkpBOYsM1rmyHve0wXJKt0xWcYjGd3kCG8x7UKy5U9dHd3CILkKd1jre%2FAZOwbe09zYf710sJ46V5KOl6nkv%2FEbkypEU3cEPW9Y%2Ffd9Rd", "mlpersist": "1017001268.1.813038960.1361820672"}
    if cookies :
        cookie_param = []
        for k, v in cookies.items() :
            cookie_param.append({'name':k,'value':v, 'url':url})
        page.run_cdp("Network.setCookies", **{
            "cookies": cookie_param
        })
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.meganslaw.ca.gov/?searchType=City',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    }
    if headers :
        page.run_cdp("Network.setExtraHTTPHeaders", **{'headers':headers})
    
    # page.listen.start('api/post/item_list/')  # 指定监听目标并启动监听
    page.get(url)
    # packet = page.listen.wait()  # 等待数据包
    # page.stop_loading()  # 主动停止加载
    # img_bytes = page.get_screenshot(as_bytes=True,full_page=False)
    # wf = open("/Users/linling/Desktop/a.png","wb")
    # wf.write(img_bytes)
    # wf.close()
    # javascript = "document.getElementById('city-only-search').value = 'LOS ANGELES';document.getElementById('submitButton').click();var c = function () {document.getElementById('continueButton').click()};setInterval('c()',8000)"
    javascript = ""
    if javascript :
        js_ret = page.run_cdp("Runtime.evaluate", **{
            "expression": javascript
        })
        js_ret = js_ret.get('result',{}).get('value')
    
    actions = [
        "{\"type\":\"javascript\",\"command\":\"document.getElementById('city-only-search').value = 'LOS ANGELES';document.getElementById('submitButton').click();\"}",
        "{\"type\":\"sleep\",\"command\":5}",
        "{\"type\":\"javascript\",\"command\":\"document.getElementById('continueButton').click()\"}",
        "{\"type\":\"sleep\",\"command\":5}",
        "{\"type\":\"javascript\",\"command\":\"document.getElementById('continueButton').click()\"}",
    ]
    if actions :
        for action in actions :
            action_kv = json.loads(action)
            k = action_kv.get('type')
            command = action_kv.get('command')
            if k == 'javascript' :
                js_ret = page.run_cdp("Runtime.evaluate", **{
                    "expression": command
                })
            elif k == 'sleep' :
                time.sleep(command)
    time.sleep(10)
    print(page.html, file=open('/Users/linling/Desktop/a.html', 'w'))  # 打印数据包正文
    








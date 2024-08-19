

from drission_page_render import DrissionPageRender
import time
import logging
import sys

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
    cookies = {".AspNetCore.Antiforgery.VyLW6ORzMgk": "CfDJ8P4MjYHqlLhAr34x3NlJZW5S_yEgzbSZI6pCaKg-_vT_NeEQE1CMfhgPU_mp5rSnuI15of2nl-ckyPcLNjwWlCyuUQ8ittteeIsI2rKmx_RCGZmQlPBVIQfHxvg2SZhbppEBRuhKeVC6zJX927Ks1k8",
               ".AspNetCore.Mvc.CookieTempDataProvider": "CfDJ8P4MjYHqlLhAr34x3NlJZW74Mqp-cVYmTB2T_toiiKzJSlNsE7OcXATBRIcrq2i8wIZ4C8AihXD4_eAEpGFbv8h0CPVo1u9pcW7H1Ko_K9bcwv9zKItMelcrI2G_Tmi8GkFJ5-X_hoSaBnDj6K3MnREt72Tvhu6hTx0oxlpuFteGcchCW5-g9ONxgQg-FzWjxWkMlGSTT_9trfU2Hh4XtuM",
               ".AspNetCore.Session": "CfDJ8P4MjYHqlLhAr34x3NlJZW7rsDT56W0YdizCgCKvTZRGRLNUT7qgugOhyVnfJXuLYh%2BQ1ASuLy7jMmgxtK3cvFprHjWtmt1n1L9s0IgkmAhrCuIvnJeo80BeFw%2BzHMrNId7PE2qv5HD%2BuHfk%2BK6qAMH%2F7kx9Jb63bT7LSO72Te55",
               "mlpersist": "43443715.1.813038960.1355738112"}
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
    javascript = ""
    if javascript :
        js_ret = page.run_cdp("Runtime.evaluate", **{
            "expression": javascript
        })
        js_ret = js_ret.get('result',{}).get('value')
        time.sleep(1)
    time.sleep(10)
    print(page.html, file=open('/Users/linling/Desktop/a.html', 'w'))  # 打印数据包正文
    








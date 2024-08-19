

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
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
with DrissionPageRender(headless=False, user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, proxy_host="http://172.28.16.140:3128", disable_proxy=True) as page :
    url = "https://www.meganslaw.ca.gov/"
    # page.set.load_mode.none()  # 设置加载模式为none
    cookies = {
        ".AspNetCore.Session":"CfDJ8P4MjYHqlLhAr34x3NlJZW6IXnZfgaeRboI5oiJsVEYc62KWyKQaatp%2B%2BL3bb%2Buhjw%2BnnB1WXGk3d7pz44yiNfpSTSl7SuySYCw8S5GUrNuTx5J0rAKeEmE3j%2BCK29XK7KWV6%2FBJcFSvtFTwKI2yzJwcpedMn8IAebM4uWV8hYcv",
         "mlpersist":"113598562.1.813038960.1332257792",
        ".AspNetCore.Antiforgery.VyLW6ORzMgk":"CfDJ8P4MjYHqlLhAr34x3NlJZW7TkVBpnY3buTpX1Ie-hbKCU0gJj9QFB_rc7Gmpg0T58-7CtJZcdJkhAlUaOHI1o_0X8eFmxXUG2f0077okdCw-mDqk8Lgu-Q257JF15Usb73YFfgg2trDsQYu_Kk7FqOc",
        ".AspNetCore.Mvc.CookieTempDataProvider":"CfDJ8P4MjYHqlLhAr34x3NlJZW6YjBo90mdeFEvbjhqQc_7DQPTUHaBNT59JhVHWcE3UiF-H1sfA14-lzYXdQIYiG53fXfFcB_L_W46KCKSS55DwJgZteKCewd3h6H_-11_JXECJkmd6P8q3F7fJysLLan1IsxtAjMYRoeNhHeiHUpUEbKFfLQiyitw0XPh2p0I9pVfjjRKgY2Iojz-hUAJ1b_Tj6b9dNyt1pj5wsmpZZK8cD0pxcaayEBK-9CLevPeBiaag7_dNS84OctqwmyZll7FVgcXcxtmCJnt4iPMv_P5W9_R_w9jJ84D900YIREy9BdvVfxDvPZIJSzYGAroCkYXNiWyHqbLFhkAHseU27u6hb8i6WTmN5kP7TToCIrdWmmNYjX36ZvqTno2b5WuWDX9iriuvuLKakPjfZNQA_0nnLoPK09Ro3DzlRTTbrfcvnQlh0kIXD21OX4ujjA2f2L8CoKhU4O-Zz0l5aZpINMC0ZPSSeIHogjDtbI5dYQ2zwEr2RpkySy6ppUm391JQdO2FdycgGMWT1tqZu23jNHntKTfBfjQWTowQgXg_5l6UiUcI_ytqcCFXGgQPBr5ZIFGJs3fIXaCEjp6k5EbSWXMhJZLqDvv97hSsUXESVlBHh9OBgSxzssa0bc4KCBmzXc2PQApxYSQqfbogX217gZtcQG6KL7WsslxjRyIqol_-qjlkVefXFg7vFjJk_xMmVH5LR04i7Qpm6ByJ_scYn_8sPOynRrdjw2wGea1aXq3r9C2AGXeVvlZqRA6E6mz9QGtekhzYysL0zrpE0BvS8xgcTw4pIeKcHf_2hVL08X-HeFke2e5DUN1rXFwUFX9AEIXtbtReA7psHKLfZLauc-67LGG0dupRN6hGhP2x_i9FFVVj5t28diOPYTY56IiUuwG7120FdPA0yqhtTuj8e9SV0rD_NV_5dgPaIrnipPY_ZD2rsZAk4OR-xYCD82u3v20"
    }
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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
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
    print(page.html, file=open('/Users/linling/Desktop/a.html', 'w'))  # 打印数据包正文
    








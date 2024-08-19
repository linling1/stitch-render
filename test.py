

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
with DrissionPageRender(headless=True, user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, proxy_host="http://172.28.16.140:3128", disable_proxy=True) as page :
    url = "https://www.meganslaw.ca.gov/"
    # page.set.load_mode.none()  # 设置加载模式为none
    cookies = {
        ".AspNetCore.Session":"CfDJ8P4MjYHqlLhAr34x3NlJZW6peLe8J%2BeHFSelfom1Z4Y0rCJAfZpb8GwR6AvsMLrGw3jnKGeb0odgWJ3ATzJZBRVtQ6RuL1thDoeWTzPxWqEp8X0KKBerVdOQ4DQW%2BgD5PWbn9ovlgxndE78W%2BOXW8mH3SM3MfOx6MrPd47%2BM9glI",
        ".AspNetCore.Antiforgery.VyLW6ORzMgk":"CfDJ8P4MjYHqlLhAr34x3NlJZW5MeuuCdakC8jLJqqldU7e2ZBbbXsS5FSHDKucD7giv9YavTvsZzef1cyVWAZbV8n1Hc80voZaxQtHtD8YdbzAjcOzrIiIEtbUpkxLpYRmo6BktZXVEvdM9PRTREASsI1Q",
        ".AspNetCore.Mvc.CookieTempDataProvider":"CfDJ8P4MjYHqlLhAr34x3NlJZW66IfYlxRpcJSwE-xaKplDL4Gghz2NPB5SRfgbCynpDLlp-Gw492iEQRsC_1VdQyBzMINnJHgfGKIiKz-sMlmjgzAC-5KHe1odjW9mM_okE2tCxkaMR4Ayo1uZyCp09vlV9zgzCOlxjSR_rWf9ELHFF02Q9Ko5N3W1HjKDwR9CRejBpLI2S-LgiJOqviEwRNKEdioyNaL0gKBa53w23HcIevMfxsD2IhTzDMFGuMGYtqU4v9YslQUzlF3fB_2Wf2nNGoleyazO8RIo_U7WOboNcUURnweRBVJZS_xAhjKvVi4lrIUzULl7GV-cqNrqPxh0U6PYr5G9A1VaUIAZ066sahodZ87RFarnucZALtNfUIanDPyulH66x7MmdwKUKGE9JFMZ01PT7ckApSkjbmnMHblggkri1Ogf1OOBfyxW3vqd5nbvFIa6eN7im4wo9zqXtsIZteUrrsqDJZFDANBeL0DvV1zX9DJkNNkANUw6uS9gp-84_-SoKE49VDacSQ9x13niUATc1eTkxi67ZW0y_qQ-skJEKxzDmdOK92BKwNYLZ_0AqRcXcLXQpxVYohvlkMWb14MbZLOBbRw7dxFCMmpCpHKlOwt1grfVfFucLseDaENapHy6NyTcKhmIyBgeU0LHPAAhsLI9XLX3VTA4VLCpBa-eHroXib__LkTcAHlfWDz98TO7pAPY9bTt3fykKZiXcBnhEnfE8rel0kmJ2Lp2TrFcwC92TqlyFX5nDBaiq7WgqPl4ENcvEWS8I3dJq-7S3nz6xHNVdxzSrJIf023ruw33RqVXKcyXj8Tl8TIqOjYhE8poTQqN0GeE5JEOn6OkNlMvzE3W_mq9JABLwfQYD6aj0r5jGDlbgQmG7y7zwBlujnopMYlKqTsF-KopsJZZNRuZM6XO-sffR1oJCKzkpDgcF491uY2G24y5w5kqaL1eR4HLbVMpUqJ441L8"
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
    time.sleep(10)
    print(page.html, file=open('/Users/linling/Desktop/a.html', 'w'))  # 打印数据包正文
    








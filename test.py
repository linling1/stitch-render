
from drission_page_render import DrissionPageRender
import time
import logging
import sys
import json
from captcha.google_recaptcha import RecaptchaSolver
from facility.fetch import requests_get_retry
from external_api.proxy import get_proxy
import random

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
)

# cookies = {}
# resp = requests_get_retry("https://www.meganslaw.psp.pa.gov/Home/TermsAndConditions", return_response=True)
# resp.raise_for_status()
# for cookie_key in resp.cookies:
#     cookies[cookie_key] = resp.cookies.get(cookie_key)

# chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_path = "/Users/linling/Desktop/chrome/mac-128.0.6613.137/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
while True :
    proxy_host = get_proxy()
    if proxy_host.startswith('http://172.28.') :
        break
# proxy_host = "http://172.28.2.3:10000"
print(f"proxy_host : {proxy_host}")
incognito = True
disable_proxy = False
with DrissionPageRender(headless=False, user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, proxy_host=proxy_host, disable_proxy=disable_proxy, incognito=incognito) as page :
    url = "https://www.xiaohongshu.com/explore"
    # page.set.load_mode.none()  # 设置加载模式为none
    # cookies = {"datadome": "rfpV3_2zpMZPuq71K6V4rontU2MCE~Mb02VMNMxc~9etqzk2WbNrbQoonjR5yeyq4m0c25XDS5Dyhynky5LwojDcvMFKFlo8tndOcDsx~uixioQTxwJR_biZtc0CMc1Y"}

    cookies = {
        "abRequestId":"d180e500-c363-5c48-b43e-8cff60518bb0",
        "a1":"18e16c4db4b3wd8mg2bq0ntzke2eardthspgwmf7z30000346645",
        "webId":"9aa00286ca96d93ca0360dcd652d5e7b",
        "gid":"yYdyKS4dJyxiyYdyKS4fDM6i4DqEfY6kJDA8UWuI9uTdJkq8d0Ff9E888q4KK428YqyyKD2W",
        "xsecappid":"xhs-pc-web",
        "web_session":"0400698d25fea93c97b6f66d64354b42ff32c9",
        "webBuild":"4.46.0",
        "acw_tc":"0a4ae08a17335717015811955e2d77ee0e4575d8ce18a593d7a96b7513f7a4",
        "websectiga":"cf46039d1971c7b9a650d87269f31ac8fe3bf71d61ebf9d9a0a87efb414b816c",
        "sec_poison_id":"e0d54528-7b29-4434-9974-ddfb6a3aeb5a"
    }
    # cookies = {}
    if cookies :
        cookie_param = []
        for k, v in cookies.items() :
            cookie_param.append({'name':k,'value':v, 'url':url})
        page.run_cdp("Network.setCookies", **{
            "cookies": cookie_param
        })
    headers = {}
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

    # javascript = "document.getElementById('confirmBtn').click();document.getElementById('zipcodes').value = '19120 19124 19143';document.getElementById('searchbynamezip').click();"
    # javascript = 'window._webmsxyw("/api/sns/web/v1/search/notes",{"keyword": "湾区","page": 1,"page_size": 20,"search_id": "2e4e5a0ps6ukgutylrb0v","sort": "general","note_type": 0})'
    javascript = ""
    if javascript :
        js_ret = page.run_js(javascript,as_expr=True)
    
    
    # actions = [
    #     # json.dumps(
    #     #     {
    #     #         "type": "javascript",
    #     #         "command": "document.querySelector('input[value=\"I Agree\"]').click()",
    #     #     }
    #     # ),
    #     # json.dumps({"type": "sleep", "command": 15}),
    #     json.dumps({"type": "reCAPTCHA"}),
    #     json.dumps(
    #         {
    #             "type": "javascript",
    #             "command": "document.querySelector('input[value=\"Continue\"]').click()",
    #         }
    #     ),
    #     json.dumps({"type": "sleep", "command": 2}),
    #     json.dumps(
    #         {
    #             "type": "retry",
    #             "command": json.dumps(
    #                 {
    #                     "type": "txt_check",
    #                     "command": "Please check the box and then press Continue.",
    #                 }
    #             ),
    #         }
    #     ),
    # ]
    actions = [
        json.dumps({"type": "sleep", "command": 2}),
        json.dumps(
            {
                "type": "javascript",
                "command": 'window._webmsxyw("/api/sns/web/v1/search/notes",{"keyword": "湾区","page": 1,"page_size": 20,"search_id": "2e4e5a0ps6ukgutylrb0v","sort": "general","note_type": 0})',
            }
        ),
    ]
    # actions = []
    
    retry = 1
    c = 0
    while c < retry :
        c += 1
        logging.info(f"===== c : {c}")
        screenshot_img_base64 = None
        if actions :
            for action in actions :
                action_kv = json.loads(action)
                k = action_kv.get('type')
                command = action_kv.get('command')
                if k == 'javascript' :
                    js_ret = page.run_js(command,as_expr=True)
                elif k == 'sleep' :
                    time.sleep(command)
                elif k == 'reCAPTCHA' :
                    s_t = time.time()
                    logging.info(f'loading reCAPTCHA cost : {time.time() - s_t}ms')
                    rs = RecaptchaSolver(page)
                    rs.solve_captcha()
                elif k == 'refresh' :
                    page.refresh()
                elif k == 'redirecting' :
                    page.get(command)
                elif k == 'screenshot_element' :
                    screenshot_img_base64 = page.ele(command).get_screenshot(as_base64='png')
                elif k == 'retry' :
                    if c != 1 :
                        continue
                    retry_command = json.loads(command)
                    if retry_command.get('type') == "txt_check" :
                        check_command = retry_command.get('command')
                        if check_command and check_command in page.html :
                            retry += 1
        
    # time.sleep(10)
    # time.sleep(3)

    print(page.html, file=open('/Users/linling/Desktop/a.html', 'w'))  # 打印数据包正文
    









from drission_page_render import DrissionPageRender
import time
import logging
import sys
import json
from captcha.google_recaptcha import RecaptchaSolver
from facility.fetch import requests_get_retry
from external_api.proxy import get_proxy

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
proxy_host = "http://172.28.16.88:3128"
print(f"proxy_host : {proxy_host}")
incognito = True
disable_proxy = False
with DrissionPageRender(headless=False, user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, proxy_host=proxy_host, disable_proxy=disable_proxy, incognito=incognito) as page :
    url = "https://www.paisemiu.com/cronaca/controlli-porta-a-porta-a-san-pio-individuati-313-evasori-tari/"
    # page.set.load_mode.none()  # 设置加载模式为none
    # cookies = {"datadome": "rfpV3_2zpMZPuq71K6V4rontU2MCE~Mb02VMNMxc~9etqzk2WbNrbQoonjR5yeyq4m0c25XDS5Dyhynky5LwojDcvMFKFlo8tndOcDsx~uixioQTxwJR_biZtc0CMc1Y"}
    cookies = {}
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
    javascript = ""
    if javascript :
        js_ret = page.run_cdp("Runtime.evaluate", **{
            "expression": javascript
        })
        js_ret = js_ret.get('result',{}).get('value')
    
    
    #################### PA ####################
    # county = "ALLEGHENY"
    # p = 20
    # page_href=f'https://www.meganslaw.psp.pa.gov/Search/CountySearchResultsAsync?page={p}&selectedCounty={county}&selectedSortBy=1&chkCountyIncarcerated=True'
    # command1 = f"document.getElementById('Countydropdown').value='{county}';document.getElementById('chkCountyIncarcerated').checked=true;document.querySelector('input[type=\"button\"]').click()"
    # command2 = "grecaptcha.ready(function () {grecaptcha.execute(siteKey, { action: 'search' }).then(function (token) {$('#GrecaptchaToken').val(token);location.href = '" + page_href + "' + '&GrecaptchaToken=' + token;});});"
    # actions = [
    #     json.dumps({"type":"javascript", "command":"document.querySelector('form[action=\"/Home/AcceptTerms\"] button').click()"}),
    #     json.dumps({"type":"sleep","command":0.5}),
    #     json.dumps({"type":"redirecting", "command":"https://www.meganslaw.psp.pa.gov/Search/CountySearch"}),
    #     json.dumps({"type":"sleep","command":1}),
    #     json.dumps({"type":"javascript", "command":command1}),
    #     json.dumps({"type":"sleep","command":1}),
    #     json.dumps({"type":"javascript", "command": command2}),
    #     json.dumps({"type":"sleep","command":8}),
    # ]
    #################### PA ####################
    
    frame_datas = []
    for frame in page.get_frames() :
        frame_datas.append(frame.html)
    # page.get_frames()[0].html = txt
    # actions = [
    #     json.dumps({"type":"javascript","command":f"document.getElementsByTagName('iframe')[0].outerHTML={txt}"}),
    #     # json.dumps({"type":"sleep","command":10}),
    # ]
    actions = []
    
    screenshot_img_base64 = None
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
            elif k == 'reCAPTCHA' :
                rs = RecaptchaSolver(page)
                rs.solve_captcha()
            elif k == 'refresh' :
                page.refresh()
            elif k == 'redirecting' :
                page.get(command)
            elif k == 'screenshot_element' :
                screenshot_img_base64 = page.ele(command).get_screenshot(as_base64='png')
    # time.sleep(10)
    time.sleep(3)

    print(page.html, file=open('/Users/linling/Desktop/a.html', 'w'))  # 打印数据包正文
    print(json.dumps(frame_datas), file=open('/Users/linling/Desktop/a.json', 'w'))  # 打印数据包正文
    








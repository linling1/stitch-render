
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

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
while True :
    proxy_host = get_proxy()
    if proxy_host.startswith('http://172.28.') :
        break
# proxy_host = "http://172.31.17.153:3128"
print(f"proxy_host : {proxy_host}")
incognito = True
with DrissionPageRender(headless=False, user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, proxy_host=proxy_host, disable_proxy=False, incognito=incognito) as page :
    url = "https://apps.colorado.gov/apps/dps/sor/search/search-advanced.jsf"
    # url = "https://www.tripadvisor.com/Search?q=bayern&geo=1&ssrc=a&searchNearby=false&searchSessionId=0017da849d2203ad.ssid&blockRedirect=true&offset=0"
    # page.set.load_mode.none()  # 设置加载模式为none
    # cookies = {"ASP.NET_SessionId": "ogce2lbzl1cumzoil4zafplb", "__RequestVerificationToken": "8LPCvaUUzZkyjQeblmUxarHrTxWi1Pvzj3q-MRdN6ER37MI8RQ5XMTbkBBF6QoXEKZ3zf4JVc5WpA9wHB6RzZ69oScuquRw3K406PDSpGNg1"}
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
    # javascript = "document.getElementById('city-only-search').value = 'LOS ANGELES';document.getElementById('submitButton').click();var c = function () {document.getElementById('continueButton').click()};setInterval('c()',8000)"
    # javascript = "grecaptcha.ready(function () {grecaptcha.execute('6Lc_P5AmAAAAABEJ5mSrBCTy8Bv66Ota5oTAsqQi', { action: 'search' }).then(function (token) {$('#GrecaptchaToken').val(token);window.prerenderData=token;});});"
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
    actions = [
        json.dumps({"type":"javascript","command":"document.getElementById('acceptForm:submitLogIn').click()"}),
        json.dumps({"type":"sleep","command":4}),
        json.dumps({"type":"javascript","command":"document.getElementById('advancedSearchForm:county').value='el paso'"}),
        json.dumps({"type":"sleep","command":4}),
        json.dumps({"type":"reCAPTCHA"}),
        json.dumps({"type":"javascript","command":"document.querySelector('input[type=\"submit\"]').click()"}),
        json.dumps({"type":"sleep","command":2})
    ]
    # actions = []
    # actions = [
    #     "{\"type\": \"javascript\", \"command\": \"document.getElementById('agreeInd1').checked=true\"}", 
    #     "{\"type\": \"reCAPTCHA\"}", 
    #     "{\"type\": \"javascript\", \"command\": \"document.querySelector('input[value=\\\"Proceed\\\"]').click()\"}", 
    #     "{\"type\": \"sleep\", \"command\": 5}",
    #     "{\"type\": \"javascript\", \"command\": \"document.getElementById('countyCode').value='MIDDLESEX';document.querySelector('form[action=\\\"countyCityZipSearchforSexOffenders.action\\\"] input[type=\\\"submit\\\"]').click()\"}"]
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
    # time.sleep(10)
    time.sleep(3)

    print(page.html, file=open('/Users/linling/Desktop/a.html', 'w'))  # 打印数据包正文
    








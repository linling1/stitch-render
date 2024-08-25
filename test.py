
from drission_page_render import DrissionPageRender
import time
import logging
import sys
import json
from captcha.google_recaptcha import RecaptchaSolver

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
)

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
with DrissionPageRender(headless=False, user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, proxy_host="http://172.28.16.140:3128", disable_proxy=True) as page :
    url = "https://www.criminaljustice.ny.gov/SomsSUBDirectory/search_index.jsp"
    # page.set.load_mode.none()  # 设置加载模式为none
    cookies = {"JSESSIONID": "0000XELVYKstQva0QRjqJVGIvKg:19m8h9rri"}
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
    javascript = ""
    if javascript :
        js_ret = page.run_cdp("Runtime.evaluate", **{
            "expression": javascript
        })
        js_ret = js_ret.get('result',{}).get('value')
    
    actions = [
        "{\"type\":\"javascript\",\"command\":\"document.getElementById('County').value=3\"}",
        "{\"type\":\"reCAPTCHA\"}",
        "{\"type\":\"javascript\",\"command\":\"document.querySelector('button[name=Submit]').click()\"}",
        "{\"type\":\"sleep\",\"command\":2}",
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
            elif k == 'reCAPTCHA' :
                rs = RecaptchaSolver(page)
                rs.solve_captcha()
    # time.sleep(10)
    print(page.html, file=open('/Users/linling/Desktop/a.html', 'w'))  # 打印数据包正文
    








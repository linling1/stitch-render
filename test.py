

from drission_page_render import DrissionPageRender
import time

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
width=414
height=896
with DrissionPageRender(headless=False, width=width, height=height,proxy_host="http://172.31.17.153:3128", user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, disable_proxy=True) as page :
    url = "https://www.stltoday.com/news/local/column/bill-mcclellan/mcclellan-after-many-years-these-missouri-siblings-found-each-other/article_b0f1a294-dc8b-11ee-8b48-8b23526f06ee.html"
    # page.set.load_mode.none()  # 设置加载模式为none
    # cookies = {
    #     "msToken": "6jm1b-46dptt04LSW_rvcGA4GMYcrNDuHxyp92JwtueYFPsA8tFiYgJZyCSmoGCxUtYi2cgpkv65rMPYniS4XcDQa7Xye3EEijp1PGXbqxah_xjxDLptvXAlmn0U7f1uWFIYfz9mLdiDvDQGlvA="
    # }
    # if cookies :
    #     cookie_param = []
    #     for k, v in cookies.items() :
    #         cookie_param.append({'name':k,'value':v, 'url':url})
    #     page.run_cdp("Network.setCookies", **{
    #         "source": cookie_param
    #     })
    # headers = {
    #     'cookie':"msToken=6jm1b-46dptt04LSW_rvcGA4GMYcrNDuHxyp92JwtueYFPsA8tFiYgJZyCSmoGCxUtYi2cgpkv65rMPYniS4XcDQa7Xye3EEijp1PGXbqxah_xjxDLptvXAlmn0U7f1uWFIYfz9mLdiDvDQGlvA="
    # }
    # if headers :
    #     page.run_cdp("Network.setExtraHTTPHeaders", **{'headers':headers})
    # page.listen.start('api/post/item_list/')  # 指定监听目标并启动监听
    page.get(url)
    # packet = page.listen.wait()  # 等待数据包
    # page.stop_loading()  # 主动停止加载
    img_bytes = page.get_screenshot(as_bytes=True,full_page=False)
    wf = open("/Users/linling/Desktop/a.png","wb")
    wf.write(img_bytes)
    wf.close()
    print(page.html)  # 打印数据包正文
    








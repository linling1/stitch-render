

from drission_page_render import DrissionPageRender

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
with DrissionPageRender(headless=True, proxy_host="http://172.31.17.153:3128", user_agent=user_agent, chrome_path=chrome_path, loading_page_timeout=30, disable_proxy=True) as page :
    url = "https://www.mouser.com/new/eaton/eaton-exla1v10-molded-inductors"
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
    print(page.html)  # 打印数据包正文
    








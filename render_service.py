
import logging
import time
import random
import json
from DrissionPage._elements.none_element import NoneElement
from pyquery import PyQuery as pq

from drission_page_render import DrissionPageRender, EXECUTOR_TIMEOUT, USER_AGENT_POOL
from external_api.proxy import get_proxy
from captcha.google_recaptcha import RecaptchaSolver



output_html = """
(() => {
    const innerText =  document.firstElementChild.getInnerHTML();
    const htmlNode = document.firstElementChild;
    const attributeNames = htmlNode.getAttributeNames();
    const attrStringList = attributeNames.map((attributeName) => (`${attributeName}="${htmlNode.getAttribute(attributeName)}"`))
    return `<html ${attrStringList.join(' ')}>${innerText}</html>`;
})()
"""

shasow_output_html = """
(() => {
    const elements = document.querySelectorAll('*');
    for (let i = 0; i < elements.length; i++) {
        const el = elements[i];
        if (el.shadowRoot) {
            var txt = el.shadowRoot.inner_html;
            el.inner_html = txt;
        }
    }
    const innerText =  document.firstElementChild.getInnerHTML({includeShadowRoots: true});
    const htmlNode = document.firstElementChild;
    const attributeNames = htmlNode.getAttributeNames();
    const attrStringList = attributeNames.map((attributeName) => (`${attributeName}="${htmlNode.getAttribute(attributeName)}"`))
    return `<html ${attrStringList.join(' ')}>${innerText}</html>`;
})()
"""

shadow_elements = """
(() => {
    shadow_elements = []
    const elements = document.querySelectorAll('*');
    for (let i = 0; i < elements.length; i++) {
        const el = elements[i];
        if (el.shadowRoot) {
            shadow_elements.push(el.outerHTML);
        }
    }
    return JSON.stringify(shadow_elements);
})()    
"""


class RenderService:
    
    def __init__(self, chrome_path:str) -> None:
        self.chrome_path = chrome_path
    
    
    def render(self, url:str, render_type:str="json", user_agent:str=None, headers:dict=None, cookies:dict=None, proxy_url:str=None, loading_page_timeout:int=EXECUTOR_TIMEOUT, refresh:bool=False, javascript:str=None, disable_proxy:bool=False, delay:float=None, width:int=1440, height:int=718, full_page:bool=False, disable_pop:bool=True, incognito:bool=True, actions:list=None, include_shasow_roots:bool=False, enable_iframe:bool=False) -> str :
        try :
            proxy_host = proxy_url if proxy_url else get_proxy()
            if proxy_url :
                proxy_host = proxy_url
            else :
                while True :
                    proxy_host = get_proxy()
                    if proxy_host.startswith('http://172.28.') :
                        break
            user_agent = user_agent if user_agent else USER_AGENT_POOL[random.randint(0, len(USER_AGENT_POOL) - 1)]
            loading_page_timeout = loading_page_timeout if loading_page_timeout else EXECUTOR_TIMEOUT
            width = width if width else 1440
            height = height if height else 718
            logging.info(f"render. url : {url} ; refresh : {refresh} ; proxy_host : {proxy_host} ; user_agent : {user_agent} ; loading_page_timeout : {loading_page_timeout} ; disable_proxy : {disable_proxy} ; javascript : {javascript}")
            with DrissionPageRender(proxy_host=proxy_host, user_agent=user_agent, loading_page_timeout=loading_page_timeout, disable_proxy=disable_proxy, width=width, height=height, chrome_path=self.chrome_path, disable_pop=disable_pop, incognito=incognito) as page :
                if cookies :
                    cookie_param = []
                    for k, v in cookies.items() :
                        cookie_param.append({'name':k,'value':v, 'url':url})
                    page.run_cdp("Network.setCookies", **{
                        "cookies": cookie_param
                    })
                
                if headers :
                    page.run_cdp("Network.setExtraHTTPHeaders", **{'headers':headers})

                status = page.get(url) 
                logging.info(f"status : {status}")
                if refresh :
                    page.refresh()
                
                js_ret = None
                if javascript :
                    js_ret = page.run_js(javascript,as_expr=True)
                
                
                screenshot_img_base64 = None
                if actions :
                    retry = 1
                    c = 0
                    while c < retry :
                        c += 1
                        for action in actions :
                            action_kv = json.loads(action)
                            k = action_kv.get('type')
                            command = action_kv.get('command')
                            if k == 'javascript' :
                                js_ret = page.run_js(command,as_expr=True)
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
                                ele = page.ele(command)
                                if type(ele) != NoneElement :
                                    screenshot_img_base64 = ele.get_screenshot(as_base64='png')
                            elif k == 'retry' :
                                if c != 1 :
                                    continue
                                retry_command = json.loads(command)
                                if retry_command.get('type') == "txt_check" :
                                    check_command = retry_command.get('command')
                                    if check_command and check_command in page.html :
                                        retry += 1
                    
                if delay and delay > 0 :
                    time.sleep(delay)
                else :
                    time.sleep(1)

                if render_type in ["png","jpeg"] :
                    content = page.get_screenshot(as_bytes=render_type,full_page=full_page)
                else :
                    print_html = shasow_output_html if include_shasow_roots else output_html
                    ret = page.run_cdp("Runtime.evaluate", **{
                        "expression": print_html
                    })
                    content = ret.get('result',{}).get('value')
                
                # resp = page.run_cdp("Network.loadNetworkResource", **{'frameId':page._frame_id,'url':page.url, 'options':{'disableCache':True,'includeCredentials':True}})
                resp = page.run_cdp("Network.loadNetworkResource", **{'frameId':page._frame_id,'url':page.url, 'options':{'disableCache':False,'includeCredentials':True}})
                logging.info(f"resp : {resp}")
                resp_cookies = page.cookies(as_dict=True)
                logging.info(f"resp_cookies : {resp_cookies}")
                
                if screenshot_img_base64 :
                    screenshot_img_base64 = f"data:image/png;base64,{screenshot_img_base64}"

                
                if enable_iframe :
                    html_dom = pq(content)
                    for frame in page.get_frames() :
                        frame_dom = pq(frame.html)
                        frame_src = frame_dom.attr('src')
                        tag = 'frame' if frame_dom.is_('frame') else 'iframe'
                        if frame_src :
                            html_dom(f'{tag}[src="{frame_src}"]:first').html(frame.inner_html)
                
                    if include_shasow_roots :
                        ret = page.run_cdp("Runtime.evaluate", **{
                            "expression": shadow_elements
                        })
                        shadows_raw = ret.get('result',{}).get('value')
                        if shadows_raw :
                            for item in json.loads(shadows_raw) :
                                tag = item.split(" ")[0][1:]
                                for e in page.eles(f"tag:{tag}") :
                                    if not e.shadow_root:
                                        continue
                                    for iframe_e in e.shadow_root.eles('tag:iframe') :
                                        frame_dom = pq(iframe_e.html)
                                        frame_src = frame_dom.attr('src')
                                        if frame_src :
                                            html_dom(f'iframe[src="{frame_src}"]:first').html(iframe_e.inner_html)

                    content = html_dom.outer_html()
                
                resp = {
                    "url": page.url,
                    "proxy": None if disable_proxy else proxy_host,
                    "userAgent": user_agent,
                    "content": content,
                    "status": resp.get('resource',{}).get('success'),
                    "httpStatusCode": resp.get('resource',{}).get('httpStatusCode'),
                    "headers": resp.get('resource',{}).get('headers'),
                    "cookies": resp_cookies,
                }
                if screenshot_img_base64 :
                    resp["screenshot_img_base64"] = screenshot_img_base64
                if js_ret :
                    resp["js_ret"] = js_ret
                return resp
        except Exception as e :
            logging.error(f"redner fail. url : {url} ; user_agent : {user_agent} ; proxy_host : {proxy_host} ; loading_page_timeout : {loading_page_timeout} . err : {e}")
            logging.exception(e)
            raise e
        








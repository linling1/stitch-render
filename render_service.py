
import logging
import time
import random
import json

from drission_page_render import DrissionPageRender, EXECUTOR_TIMEOUT, USER_AGENT_POOL
from external_api.proxy import get_proxy
from captcha.google_recaptcha import RecaptchaSolver


output_html = """
(() => {
    const innerText =  document.firstElementChild.getInnerHTML({includeShadowRoots: true});
    const htmlNode = document.firstElementChild;
    const attributeNames = htmlNode.getAttributeNames();
    const attrStringList = attributeNames.map((attributeName) => (`${attributeName}="${htmlNode.getAttribute(attributeName)}"`))
    return `<html ${attrStringList.join(' ')}>${innerText}</html>`;
})()
"""


class RenderService:
    
    def __init__(self, chrome_path:str) -> None:
        self.chrome_path = chrome_path
    
    
    def render(self, url:str, render_type:str="json", user_agent:str=None, headers:dict=None, cookies:dict=None, proxy_url:str=None, loading_page_timeout:int=EXECUTOR_TIMEOUT, refresh:bool=False, javascript:str=None, disable_proxy:bool=False, delay:float=None, width:int=1440, height:int=718, full_page:bool=False, disable_pop:bool=True, incognito:bool=True, actions:list=None) -> str :
        try :
            proxy_host = proxy_url if proxy_url else get_proxy()
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
                    js_ret = page.run_cdp("Runtime.evaluate", **{
                        "expression": javascript
                    })
                    js_ret = js_ret.get('result',{}).get('value')
                
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
                    
                if delay and delay > 0 :
                    time.sleep(delay)
                else :
                    time.sleep(1)

                if render_type in ["png","jpeg"] :
                    content = page.get_screenshot(as_bytes=render_type,full_page=full_page)
                else :
                    ret = page.run_cdp("Runtime.evaluate", **{
                        "expression": output_html
                    })
                    content = ret.get('result',{}).get('value')
                
                resp = page.run_cdp("Network.loadNetworkResource", **{'frameId':page._frame_id,'url':page.url, 'options':{'disableCache':True,'includeCredentials':True}})
                logging.info(f"resp : {resp}")
                

                return {
                    "url": page.url,
                    "proxy": None if disable_proxy else proxy_host,
                    "userAgent": user_agent,
                    "content": content,
                    "status": resp.get('resource',{}).get('success'),
                    "httpStatusCode": resp.get('resource',{}).get('httpStatusCode'),
                    "headers": resp.get('resource',{}).get('headers'),
                }
        except Exception as e :
            logging.error(f"redner fail. url : {url} ; user_agent : {user_agent} ; proxy_host : {proxy_host} ; loading_page_timeout : {loading_page_timeout} . err : {e}")
            logging.exception(e)
            raise e
        








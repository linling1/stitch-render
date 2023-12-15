
import logging
import time
import random

from selenium_render import SeleniumRender, EXECUTOR_TIMEOUT, USER_AGENT_POOL
from external_api.proxy import get_proxy


output_html = """
(() => {
    const innerText =  document.firstElementChild.getInnerHTML({includeShadowRoots: true});
    const htmlNode = document.firstElementChild;
    const attributeNames = htmlNode.getAttributeNames();
    const attrStringList = attributeNames.map((attributeName) => (`${attributeName}="${htmlNode.getAttribute(attributeName)}"`))
    return `<html ${attrStringList.join(' ')}>${innerText}</html>`;
})()
"""


def render(url:str, user_agent:str=None, cookies:dict=None, proxy_url:str=None, loading_page_timeout:int=EXECUTOR_TIMEOUT, refresh:bool=False, javascript:str=None, disable_proxy:bool=False, delay:float=None, width:int=1440, height:int=718) -> str :
    try :
        proxy_host = proxy_url if proxy_url else get_proxy()
        user_agent = user_agent if user_agent else USER_AGENT_POOL[random.randint(0, len(USER_AGENT_POOL) - 1)]
        loading_page_timeout = loading_page_timeout if loading_page_timeout else EXECUTOR_TIMEOUT
        width = width if width else 1440
        height = height if height else 718
        with SeleniumRender(proxy_host=proxy_host, user_agent=user_agent, loading_page_timeout=loading_page_timeout, disable_proxy=disable_proxy, width=width, height=height) as driver :
            if cookies :
                cookie_param = []
                for k, v in cookies :
                    cookie_param.append({'name':k,'value':v, 'url':url})
                driver.execute_cdp_cmd("Network.setCookies", {
                    "source": cookie_param
                })

            driver.get(url)
            if refresh :
                driver.refresh()
            delay = delay if delay else 0.5
            time.sleep(delay)
            
            js_ret = None
            if javascript :
                js_ret = driver.execute_cdp_cmd("Runtime.evaluate", {
                    "expression": javascript
                })
                js_ret = js_ret.get('result',{}).get('value')
                time.sleep(1)

            ret = driver.execute_cdp_cmd("Runtime.evaluate", {
                "expression": output_html
            })
            html = ret.get('result',{}).get('value')
            
            return {
                "url": driver.current_url,
                "proxy": None if disable_proxy else proxy_host,
                "userAgent": user_agent,
                "content": html
            }
    except Exception as e :
        logging.error(f"redner fail. url : {url} ; user_agent : {user_agent} ; cookies : {cookies} ; proxy_host : {proxy_host} ; loading_page_timeout : {loading_page_timeout} . err : {e}")
        logging.exception(e)
        raise e
        








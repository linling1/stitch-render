
import logging
import time

from selenium_render import SeleniumRender, EXECUTOR_TIMEOUT
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




def redner(url:str, user_agent:str=None, cookies:dict=None, proxy_host:str=None, loading_page_timeout:int=EXECUTOR_TIMEOUT, refresh:bool=False, javascript:str=None) -> str :
    try :
        proxy_host = proxy_host if proxy_host else get_proxy()
        with SeleniumRender(proxy_host=proxy_host, user_agent=user_agent, loading_page_timeout=loading_page_timeout) as driver :
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
                time.sleep(1)
            
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
            return html
    except Exception as e :
        logging.error(f"redner fail. url : {url} ; user_agent : {user_agent} ; cookies : {cookies} ; proxy_host : {proxy_host} ; loading_page_timeout : {loading_page_timeout} . err : {e}")
        logging.exception(e)
        raise e
        








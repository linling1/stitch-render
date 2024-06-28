import logging
import os
from DrissionPage import ChromiumPage, ChromiumOptions
import time


USER_AGENT_POOL = [
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
    "Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Exabot-Thumbnails)",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
]

EXECUTOR_TIMEOUT = 20


class DrissionPageRender:
    
    def __init__(self, headless=True, proxy_host=None, run_js:bool=True, user_agent:str=None, loading_page_timeout:int=EXECUTOR_TIMEOUT, disable_proxy:bool=False, width:int=1440, height:int=718, chrome_path:str=None, disable_pop:bool=True, incognito:bool=True) -> None :
        self.page = self._get_page(headless=headless, proxy_host=proxy_host, run_js=run_js, user_agent=user_agent, loading_page_timeout=loading_page_timeout, disable_proxy=disable_proxy, width=width, height=height, chrome_path=chrome_path, disable_pop=disable_pop, incognito=incognito)
        
    def _get_page(self, headless=True, mobile=False, proxy_host=None, run_js:bool=False, user_agent:str=None, loading_page_timeout:int=EXECUTOR_TIMEOUT, disable_proxy:bool=False, width:int=1440, height:int=718, chrome_path:str=None, disable_pop:bool=True, incognito:bool=True) -> ChromiumPage :
        page = None
        try :
            co = ChromiumOptions(ini_path="./config/dp_configs.ini")
            co.clear_arguments()
            co.clear_flags()
            co.set_pref('excludeSwitches', ['enable-automation','enable-logging'])
            co.set_pref('useAutomationExtension', False)
            co.set_pref('prefs', {'intl.accept_languages': 'en,en_US'})
            co.set_pref('goog:loggingPrefs', { 'browser':'ALL' })
            
            if headless :
                co.headless(True)
            else :
                co.set_argument("--headless", 'false')
            
            if mobile :
                co.set_pref('mobileEmulation', { "deviceName": "iPhone XR" })
            else :
                co.set_user_agent(user_agent)
            
            if disable_pop  :
                co.set_argument("--disable-notifications")
                co.set_argument("--disable-popup-blocking")
            
            if incognito :
                co.set_argument("--incognito")
            
            co.set_argument("--disable-blink-features", "AutomationControlled")
            co.set_argument("--disable-dev-shm-usage")
            co.set_argument("--start-maximized")
            # co.set_argument("--no-sandbox")
            # co.set_argument("--ignore-certificate-errors")
            co.set_argument("--log-level", '3')
            co.set_argument('--window-size', f'{width},{height}')
            co.set_argument("--profile-directory", "Default")
            co.set_argument("--disable-plugins-discovery")
            co.set_argument("--lang", "en-US")
            co.ignore_certificate_errors(True)
            co.set_timeouts(page_load=loading_page_timeout)
            
            if proxy_host is not None and not disable_proxy :
                co.set_proxy(proxy_host)
            
            if chrome_path :
                co.set_browser_path(chrome_path)
            
            co.auto_port()
            page = ChromiumPage(co)
            if run_js :
                js = open(os.path.join(os.path.dirname(__file__), './js/stealth.min.js')).read()
                page.run_cdp("Page.addScriptToEvaluateOnNewDocument", **{
                    "source": js
                })
            
            return page
        except Exception as e:
            try :
                page.quit()
            except :
                pass
            raise e

        
    def close(self) -> None :
        print("========= close =========")
        if self.page :
            try :
                self.page.quit()
            except :
                pass
    
    def __enter__(self) :
        return self.page
    
    def __exit__(self, *args) :
        self.close()        
        
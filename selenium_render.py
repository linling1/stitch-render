import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random


USER_AGENT_POOL = [
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
    "Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Exabot-Thumbnails)",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
]

EXECUTOR_TIMEOUT = 20

class SeleniumRender :
    
    def __init__(self, headless=True, proxy_host=None, run_js:bool=True, user_agent:str=None, loading_page_timeout:int=EXECUTOR_TIMEOUT, disable_proxy:bool=False, width:int=1440, height:int=718, chrome_path:str=None, version:str=None) -> None :
        self.driver = self._get_driver(headless=headless, proxy_host=proxy_host, run_js=run_js, user_agent=user_agent, loading_page_timeout=loading_page_timeout, disable_proxy=disable_proxy, width=width, height=height, chrome_path=chrome_path, version=version)
    
    
    def _get_driver(self, headless=True, mobile=False, proxy_host=None, run_js:bool=False, user_agent:str=None, loading_page_timeout:int=EXECUTOR_TIMEOUT, disable_proxy:bool=False, width:int=1440, height:int=718, chrome_path:str=None, version:str=None) -> webdriver.Chrome :
        try :
            chrome_options = webdriver.ChromeOptions()
            if headless:
                chrome_options.add_argument("--headless=new")

            if mobile:
                # use to load as mobile
                mobile_emulation = { "deviceName": "iPhone XR" }
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            else:
                chrome_options.add_argument(
                    f'--user-agent={user_agent}'
                )

            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 就是这一行告诉chrome去掉了webdriver痕迹，令navigator.webdriver=false，极其关键
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument('--ignore-certificate-errors')
            # chrome_options.add_argument('--disable-gpu')
            # chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument(f'--window-size={width},{height}')
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--profile-directory=Default")
            chrome_options.add_argument("--disable-plugins-discovery")
            chrome_options.add_argument('--lang=en-US')
            chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            capabilities = dict(DesiredCapabilities.CHROME)
            if proxy_host is not None and not disable_proxy:
                capabilities['proxy'] = {
                    'proxyType': 'MANUAL',
                    'httpProxy': proxy_host,
                    'sslProxy': proxy_host,
                    'noProxy': '',
                    'class': "org.openqa.selenium.Proxy",
                    'autodetect': False
                }
            capabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

            if chrome_path :
                chrome_options.binary_location = chrome_path
                driver = webdriver.Chrome(service=Service(ChromeDriverManager(version=version).install()),
                                            options=chrome_options, desired_capabilities=capabilities)
            else :
                driver = webdriver.Chrome(service=Service(ChromeDriverManager(version=version).install()),
                                            options=chrome_options, desired_capabilities=capabilities)
            
            if run_js :
                js = open(os.path.join(os.path.dirname(__file__), './js/stealth.min.js')).read()
                driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": js
                })
                
            driver.set_page_load_timeout(loading_page_timeout)
                
            return driver
        except :
            try :
                driver.quit()
            except :
                pass
    
    
    def close(self) -> None :
        print("========= close =========")
        if self.driver :
            try :
                self.driver.quit()
            except :
                pass

    
    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    
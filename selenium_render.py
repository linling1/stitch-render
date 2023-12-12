import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



class SeleniumRender :
    
    def __init__(self, headless=True, proxy_host=None, run_js:bool=True) -> None :
        self.driver = self._get_driver(headless=headless, proxy_host=proxy_host, run_js=run_js)
    
    
    def _get_driver(self, headless=True, mobile=False, proxy_host=None, run_js:bool=False) -> webdriver.Chrome :
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")

        if mobile:
            # use to load as mobile
            mobile_emulation = { "deviceName": "iPhone XR" }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        else:
            chrome_options.add_argument(
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            )

        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 就是这一行告诉chrome去掉了webdriver痕迹，令navigator.webdriver=false，极其关键
        # chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        capabilities = dict(DesiredCapabilities.CHROME)
        if proxy_host is not None:
            capabilities['proxy'] = {
                'proxyType': 'MANUAL',
                'httpProxy': proxy_host,
                'sslProxy': proxy_host,
                'noProxy': '',
                'class': "org.openqa.selenium.Proxy",
                'autodetect': False
            }

        driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="113.0.5672.63").install()),
                                        options=chrome_options, desired_capabilities=capabilities)
        # driver.set_page_load_timeout(EXECUTOR_TIMEOUT)
        if run_js :
            js = open(os.path.join(os.path.dirname(__file__), './js/stealth.min.js')).read()
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js
            })
        return driver
    
    
    def close(self) -> None :
        print("close=========")
        if self.driver :
            self.driver.quit()
    
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co.headless(True)
co.set_argument("--disable-blink-features=AutomationControlled")
co.set_argument("--no-sandbox")
co.set_browser_path("/chrome/linux-128.0.6613.137/chrome-linux64/chrome")

brower = ChromiumPage(co)


tab = brower.latest_tab
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}
# if headers :
#     tab.run_cdp("Network.setExtraHTTPHeaders", **{'headers':headers})
tab.set.headers(headers)
# 跳转到登录页面
tab.get('https://www.google.com/search?q=bayern')

print(tab.title)

print(tab.html, file=open('a.html','w'))

tab.get_screenshot(path='./', name='drissionpage_screenshot.jpg')
brower.quit()
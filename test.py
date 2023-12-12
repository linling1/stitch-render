import undetected_chromedriver as uc




driver = uc.Chrome(headless=False, browser_executable_path="./chrome/linux-113.0.5672.63/chrome-linux64/chrome")
driver.get('https://nowsecure.nl')
# driver.save_screenshot('nowsecure.png')
print("------------")




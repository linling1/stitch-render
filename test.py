
from selenium_render import SeleniumRender
import time
with SeleniumRender(headless=False) as driver :
    driver.get('https://www.tiktok.com/@fcbayern')
    print("============")
    # driver.refresh()
    driver.get('https://www.tiktok.com/@fcbayern')
    time.sleep(1)
    print("============")
    
    output_html = """
    (() => {
        const innerText =  document.firstElementChild.getInnerHTML({includeShadowRoots: true});
        const htmlNode = document.firstElementChild;
        const attributeNames = htmlNode.getAttributeNames();
        const attrStringList = attributeNames.map((attributeName) => (`${attributeName}="${htmlNode.getAttribute(attributeName)}"`))
        return `<html ${attrStringList.join(' ')}>${innerText}</html>`;
    })()
    """
    ret = driver.execute_cdp_cmd("Runtime.evaluate", {
        "expression": output_html
    })
    html = ret.get('result',{}).get('value')
    print(html, file=open('./a.html','w'))








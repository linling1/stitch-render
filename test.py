
from selenium_render import SeleniumRender

with SeleniumRender(headless=False, proxy_host="http://172.31.17.153:3128") as driver :
    driver.get('https://www.nextdish.com/menu')
    
    # Object.keys(window).forEach(key => {
    #     if (/on/.test(key)) {
    #         console.log(`${key.slice(2)}`)
    #         window.addEventListener(key.slice(2), event => {
    #             console.log(event);
    #             console.log(`${event.type} ; ${event.clientX} ; ${event.clientY}`)
    #         });
    #     }
    # });


    # ['blur','change','cancel','click','close','dblclick','focus','keydown','keypress','keyup','mousedown','mouseenter','mouseleave','mousemove','mouseout','mouseover','mouseup','mousewheel','submit','select','pointerdown','pointermove','pointerrawupdate','pointerup','pointercancel','pointerover','pointerout','pointerenter','pointerleave'].forEach(key => {
    #     window.addEventListener(key, event => {
    #             console.log(event);
    #             console.log(`${event.type} ; ${event.clientX} ; ${event.clientY}`)
    #         });
    # });

    driver.execute_script(script="""
            ['blur','change','cancel','click','close','dblclick','focus','keydown','keypress','keyup','mousedown','mouseenter','mouseleave','mousemove','mouseout','mouseover','mouseup','mousewheel','submit','select','pointerdown','pointermove','pointerrawupdate','pointerup','pointercancel','pointerover','pointerout','pointerenter','pointerleave'].forEach(key => {
        window.addEventListener(key, event => {
                console.log(`${event.type} ; ${event.clientX} ; ${event.clientY}`)
            });
    });
    """)
    print("============ 操作界面 ============")
    opt_logs = driver.get_log('browser')
    # 打印所有的 event 事件
    print(opt_logs)








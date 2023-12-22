
from selenium_render import SeleniumRender


with SeleniumRender(headless=False, proxy_host="http://172.31.17.153:3128") as driver :
    driver.get('https://www.nextdish.com/menu')
    print("============ 执行js ============")
    driver.execute_script(script="""
            ['blur','change','cancel','click','close','dblclick','focus','keydown','keypress','keyup','mousedown','mouseenter','mouseleave','mouseup','submit','select','pointerdown','pointerup','pointercancel','pointerenter','pointerleave'].forEach(key => {
                window.addEventListener(key, event => {
                        let target_info = null;
                        let target_ele = event.target;
                        if (target_ele) {
                            target_info = {"localName":target_ele.localName,"className":event.target.classList.value,"target":target_ele.localName+"."+target_ele.classList.value.replaceAll(' ','.')}; 
                        }
                        console.log(`event_type : ${event.type} ; target : ${JSON.stringify(target_info)} ; pageX : ${event.pageX} ; pageY : ${event.pageY}`)
                    });
            });
    """)
    print("============ 操作界面 ============")
    opt_logs = driver.get_log('browser')
    events_log = []
    # 打印所有的 event 事件. 过滤 level == 'INFO' 的相关信息
    for item in opt_logs :
        if item.get('level') != 'INFO' :
            continue
        print(item.get('message'))








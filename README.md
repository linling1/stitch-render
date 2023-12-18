Stitch Selenium Render
===========================

基于 selenium 的动态渲染


## Api

同时支持 GET 、POST 请求。

**API** : `http://172.31.16.183:3001/selenium/render`

### 请求参数

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| url | string | - | |
| userAgent | string | - | |
| width | int | 1440 | window.screen.width |
| height | int | 718 | window.screen.height |
| loading_page_timeout | int | 20 | unit : second ; waiting page loading time |
| javascript | string | - | extra exec javascript by dump page before |
| delay | int | - | unit : second ; waiting some time fater page last request |
| proxy_url | string | - | specify proxyUrl to used. e.g. `http://172.31.17.153:3128` ; if not setting, use proxy url from proxy pool by random. |
| disable_proxy | string | false | disable proxy ; if true, will be ignore `proxyUrl` param |
| cookies | string | - | customize cookie, post request is dict ; get request is array string, one cookie format `key=value`, multi kv use `;` segmentation ; e.g. get request : `cookies=PREF:tz%3DAsia.Shanghai%26hl%3Des-US` |
| refresh | bool | false | if need refresh page |


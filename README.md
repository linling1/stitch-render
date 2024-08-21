Stitch DrissionPage Render
===========================

基于 DrissionPage 的动态渲染


## Api

同时支持 GET 、POST 请求。

**API** : `http://172.31.16.183:3001/drission_page/render`

### 请求参数

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| render_type | string | json | response structure mode; support : `html` , `json` , `png` , `jpeg`. |
| url | string | - | |
| user_agent | string | random by USER_AGENT_POOL | |
| width | int | 1440 | window.screen.width |
| height | int | 718 | window.screen.height |
| loading_page_timeout | int | 20 | unit : second ; waiting page loading time |
| javascript | string | - | extra exec javascript by dump page before |
| delay | int | - | unit : second ; waiting some time fater page last request |
| proxy_url | string | - | specify proxyUrl to used. e.g. `http://172.31.17.153:3128` ; if not setting, use proxy url from proxy pool by random. |
| disable_proxy | string | false | disable proxy ; if true, will be ignore `proxyUrl` param |
| cookies | dict/string | - | customize cookie, post request is dict ; get request is array string, one cookie format `key:value`, multi kv use `;` segmentation ; e.g. get request : `cookies=PREF:tz%3DAsia.Shanghai%26hl%3Des-US` |
| headers | dict/string | - | customize headers, post request is dict ; get request is array string, one header format `key:value`, multi kv use `;` segmentation ; e.g. get request : `headers=referer:https://www.youtube.com/hashtag/funnydogs/shorts` |
| refresh | bool | false | if need refresh page |
| full_page | bool | false | avalid by render_type is `png` or `jpeg`, if screenshot full page |
| disable_pop | bool | true | |
| incognito | bool | true | |


## 验证码
### 支持验证码

#### google reCAPTCHA

* 必须安装 `ffmpeg`
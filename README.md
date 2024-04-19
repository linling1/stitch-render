
Stitch Render
===========================

基于 [prerender](https://github.com/prerender/prerender/tree/master) 的二次开发


## Api

同时支持 GET 、POST 请求。

**API** : `http://172.31.16.183:3000/render`

### 请求参数

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| url | string | - | |
| renderType | string | html | response structure mode; support : `html` , `json` , `png` , `jpeg` , `pdf` |
| userAgent | string | - | |
| width | int | 1440 | window.screen.width |
| height | int | 718 | window.screen.height |
| followRedirects | bool | false | Whether Chrome follows a redirect on the first request if a redirect is encountered |
| javascript | string | - | extra exec javascript by dump page before |
| sunflower | string | false | attatch `surface_vision_info`,`dom_style_info`,`text_vision_info` attributes to element |
| disableImage | string | false | disable fetch image |
| delay | int | - | unit : second ; waiting some time fater page last request |
| pageLoadTimeout | int | 20 | unit : second ; waiting page loading time |
| parseShadowDom | string | false | if html dump with shadow |
| proxyUrl | string | - | specify proxyUrl to used. e.g. `http://172.31.17.153:3128` ; if not setting, use proxy url from proxy pool by random. |
| disableProxy | string | false | disable proxy ; if true, will be ignore `proxyUrl` param |
| disableJS | string | false | whether script execution should be disabled |
| cookies | dict/array string | - | customize cookie, post request is dict ; get request is array string, one cookie format `key : value` ; e.g. get request : `cookies=PREF:tz%3DAsia.Shanghai%26hl%3Des-US` |
| adblock ![](https://p.ipic.vip/fklc5f.png) | string | false | whether block ad |
| interceptionStr | string | - | interception url include interceptionStr and additional response interception requestion body |
| htmlContent | string | - | html content to viewer |
| headers | dict/array string | - | customize headers, post request is dict ; get request is array string, one header format `key : value` ; e.g. get request : `headers=referer:https://www.youtube.com/hashtag/funnydogs/shorts` |
| reflush | bool | - | after loaded page to reflush page |



## Cases

* 新闻页

~~~
http://172.31.16.183:3000/render?renderType=json&disableImage=true&sunflower=true&url=https://www.iowapublicradio.org/news-from-npr/2023-09-21/biden-is-telling-his-donors-that-trump-is-out-to-destroy-democracy
~~~

* YouTube 获取评论 element

~~~
http://172.31.16.183:3000/render?disableImage=true&renderType=json&parseShadowDom=true&delay=5&javascript=scrollBy(0,%20400);&url=https://www.youtube.com/watch?v=APc8onwaSyc
~~~

* rottentomatoes

~~~
http://172.31.16.183:3000/render?renderType=json&parseShadowDom=true&url=https://www.rottentomatoes.com/m/the_nun_ii
~~~

* 拦截器示例

~~~
http://172.31.16.183:3000/render?renderType=json&delay=5&interceptionStr=/graphql/gql_para_POST&url=https%3A%2F%2Fwww.quora.com%2Fsearch%3Fq%3Dbayern
~~~
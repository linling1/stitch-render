
Stitch Render
===========================

fork from [prerender](https://github.com/prerender/prerender/tree/master)


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
| parseShadowDom | string | false | if html dump with shadow |
| proxyUrl | string | - | specify proxyUrl to used. e.g. `http://172.31.17.153:3128` ; if not setting, use proxy url from proxy pool by random. |
| disableProxy | string | false | disable proxy ; if true, will be ignore `proxyUrl` param |
| disableJS | string | false | whether script execution should be disabled |
| adblock ![](https://p.ipic.vip/og9z6b.png) | string | false | whether block ad |



## Cases

### Youtube

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


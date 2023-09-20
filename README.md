


## Cases

### Youtube

* 获取评论 element 的视频页

~~~
http://172.31.16.183:3000/render?disable_image=true&renderType=json&parseShadowDom=true&delay=5&javascript=scrollBy(0,%20400);&url=https://www.youtube.com/watch?v=APc8onwaSyc
~~~

* rottentomatoes

~~~
http://172.31.16.183:3000/render?renderType=json&parseShadowDom=true&url=https://www.rottentomatoes.com/m/the_nun_ii
~~~


> 共同问题，ShadowDom 后的内容结果和浏览器中看到的不一样。有时候还会丢失内容
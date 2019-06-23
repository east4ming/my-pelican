Title: NGINX 学习笔记-Gzip压缩-`ngx_http_gzip_module`
Category: DevOps
Date: 2019-06-23 16:33
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的NGINX服务器Gzip压缩部分. 本文介绍NGINX `ngx_http_gzip_module` 模块.
Image: /images/nginx-logo.png

本系列文章主要讨论与gzip 压缩相关的Nginx 指令.

> 相关模块: `ngx_http_gzip_module ngx_http_gzip_static_module ngx_http_gunzip_module`

## 1 ngx_http_gzip_module

1. `gzip on | off`
2. `gzip_buffers`

   用于设置Gzip压缩文件使用缓存空间的大小.

   `gzip_buffers number size;    # number 缓存空间个数; size 每个空间大小`

   默认*number × size* 为128. size的值推荐取系统内存页一页的大小, 为4KB 或者8KB. 即`gzip_buffers 32 4k | 16 8k`

3. `gzip_comp_level`

   设定Gzip压缩程度, 包括1到9. 1压缩程度最低, 9最高. 默认为1.

4. `gzip_disable`

   > :notebook:备注
   >
   >针对不同种类客户端发起的请求, 可以选择性地开启和关闭gzip功能.
   >
   > PC端：
   >
   > safari 5.1 – MAC
   >
   > User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 > (KHTML, like Gecko) Version/5.1 Safari/534.50
   >
   > safari 5.1 – Windows
   >
   > User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, > like Gecko) Version/5.1 Safari/534.50
   >
   > IE 9.0
   >
   > User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;
   >
   > IE 8.0
   >
   > User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)
   >
   > IE 7.0
   >
   > User-Agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
   >
   > IE 6.0
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
   >
   > Firefox 4.0.1 – MAC
   >
   > User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 > Firefox/4.0.1
   >
   > Firefox 4.0.1 – Windows
   >
   > User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1
   >
   > Opera 11.11 – MAC
   >
   > User-Agent:Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/> 11.11
   >
   > Opera 11.11 – Windows
   >
   > User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11
   >
   > Chrome 17.0 – MAC
   >
   > User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, > like Gecko) Chrome/17.0.963.56 Safari/535.11
   >
   > 傲游（Maxthon）
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)
   >
   > 腾讯TT
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)
   >
   > 世界之窗（The World） 2.x
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)
   >
   > 世界之窗（The World） 3.x
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)
   >
   > 搜狗浏览器 1.x
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X > MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)
   >
   > 360浏览器
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)
   >
   > Avant
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)
   >
   > Green Browser
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)
   >
   > 移动设备端：
   >
   > safari iOS 4.33 – iPhone
   >
   > User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) > AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5
   >
   > safari iOS 4.33 – iPod Touch
   >
   > User-Agent:Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/> 533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5
   >
   > safari iOS 4.33 – iPad
   >
   > User-Agent:Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/> 533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5
   >
   > Android N1
   >
   > User-Agent: Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) > AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1
   >
   > Android QQ浏览器 For android
   >
   > User-Agent: MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/> GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/> 533.1
   >
   > Android Opera Mobile
   >
   > User-Agent: Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) > Presto/2.8.149 Version/11.10
   >
   > Android Pad Moto Xoom
   >
   > User-Agent: Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/> 534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13
   >
   > BlackBerry
   >
   > User-Agent: Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, > like Gecko) Version/6.0.0.337 Mobile Safari/534.1+
   >
   > WebOS HP Touchpad
   >
   > User-Agent: Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 > (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0
   >
   > Nokia N97
   >
   > User-Agent: Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/> MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124
   >
   > Windows Phone Mango
   >
   > User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; > IEMobile/9.0; HTC; Titan)
   >
   > UC无
   >
   > User-Agent: UCWEB7.0.2.37/28/999
   >
   > UC标准
   >
   > User-Agent: NOKIA5700/ UCWEB7.0.2.37/28/999
   >
   > UCOpenwave
   >
   > User-Agent: Openwave/ UCWEB7.0.2.37/28/999
   >
   > UC Opera
   >
   > User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999
   >

   示例:

   `gzip_disable MSIE [4-6]\.`

5. `gzip_http_version`

   `gzip_http_version 1.0 | 1.1` 默认设置为1.1版本.即只有客户端使用1.1及以上版本的HTTP协议时, 才使用Gzip功能. 一般使用默认值.

6. `gzip_min_length`

   如果压缩很小的数据, 可能出现越压缩数据量越大的情况. 因此根据响应页面的大小, 选择性地开启或者关闭Gzip功能. 该指令设置页面的字节数. **响应页面的大小通过HTTP响应头部中的Content-Length指令获取, 但是如果使用了Chunk 编码动态压缩, Content-Length或不存在或被忽略, 该指令不起作用**. 默认设置为20. 设置为0时统统压缩. 建议该值为**1KB或以上**.

   `gzip_min_length 1024`

7. `gzip_proxied`

   该指令在使用Nginx服务器的反向代理功能时有效, 前提是在后端服务器返回的响应页头部中, Requests 部分包含用于通知代理服务器的Via头域.  主要用于设置Nginx服务器是否对后端服务器返回的结果进行Gzip压缩.

```
Syntax:    gzip_proxied off | expired | no-cache | no-store | private |no_last_modified | no_etag | auth | any ...;
Default:    gzip_proxied off;
Context:    http, server, location
```

- off 关闭, 默认设置;
- expired 当后端服务器响应页头部包含用于支持响应数据过期事件的expired头域时, 启用Gzip.
- no-cache 当后端包含Cache-Control头域, 且其指令值为no-cache时, 启用.
- no-store 当后端包含Cache-Control头域, 且其指令值为no-store时, 启用.
- private 当后端包含Cache-Control头域, 且其指令值为private时, 启用.
- no_last_modified 当后端服务器响应头不包含用于指明需要获取数据最后修改时间的Last-Modified 域时, 启用.
- no_etag 不包含ETag时, 启用.
- auth 包含Authorization, 启用
- any 无条件启用压缩.

8. `gzip_types`

   根据响应页的MIME类型选择性地开启Gzip压缩功能.  默认为text/html. 还可以取'*', 表示对所有MIME类型进行Gzip压缩. 推荐设置:(通常文本/图片/js都可以压缩)

   `gzip_types       text/plain application/x-javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png;`

9. `gzip_vary`

   默认为off. 推荐开启. 开启后的效果实在响应头部添加了Accept-Encoding: gzip, 这对于本身不支持Gzip压缩的客户端浏览器是有用的.

   也可以通过add_header达到相同的效果:`add_header Vary Accept-Encoding gzip;`

   > :heavy_exclamation_mark: 该指令在使用过程中存在bug, 会导致IE4及以上的浏览器的数据缓存功能失效.

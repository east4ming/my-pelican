Title: 在NGINX中根据用户真实IP进行限制
Status: published
Tags: nginx, 最佳实践
Date: 2019-10-12 17:00
Author: 东风微鸣
Slug: deny-xff-ip-in-nginx
Summary: 最近有个需求, 需要根据用户的真实IP进行限制, 但是NGINX前边还有个F5, 导致`deny`指令不生效, 最终通过其他方法实现限制.
Image: /images/nginx-logo.png



![NGINX LOGO](images/nginx-logo.png)

## 需求

**需要根据用户的真实IP进行限制, 但是NGINX前边还有个F5, 导致`deny`指令不生效.** 

阻止用户的真实IP**不是**`192.168.14.*`和`192.168.15.*`的访问请求.

## 实现

> :notebook: 备注:
>
> 关于`deny`指令的使用, 请参见我的另一篇文章: [NGINX 实战手册-安全-访问控制]({filename}/DevOps/nginx-handbook-2-1-control-access.md)

最简单的实现如下:

> :notebook: 前置条件:
>
> 需要nginx前边的load balancer设备(如F5)开启`X-Forwarded-For`支持.

```nginx
proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;

if ($proxy_add_x_forwarded_for !~ "192\.168\.1[45]")  {
    return 403;
}      
```

说明如下:

- `proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;` 获取请求头`X-Forwarded-For`中的用户真实IP, 并附加到`$proxy_add_x_forwarded_for`变量
- `if...` 
    - `(...)` 变量`$proxy_add_x_forwarded_for` 不匹配正则`192\.168\.1[45]` (即`192.168.14.*`和`192.168.15.*`)
    - `return 403`, 如果上边的条件满足, 返回403
    - 即: 如果真实IP不是`192.168.14.*`和`192.168.15.*`, 返回403.



如果有更复杂的需求, 可以参考这个示例:

```nginx
proxy_set_header HOST $http_host;
proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;

if ($http_host ~ "yourdomain.hypernode.io:8443")  {
  set $block_me_now A;
}
 
if ($proxy_add_x_forwarded_for != YOURIP) {
  set $block_me_now "${block_me_now}B";
}
 
 
if ($block_me_now = AB) {
    return 403;
    break;
}
```

## 为啥`deny`配置不起作用?

 :thinking:疑问: 为啥以下的配置不起作用?

```nginx
allow 192.168.14.0/24;
allow 192.168.15.0/24;
deny all;
```



根据nginx官方文档, `deny`指令是根据" client address"进行限制的.

> :notebook: 引用:
>
> The `ngx_http_access_module` module allows limiting access to certain **client addresses**.

而" client address" 对应的变量是: `$remote_addr`

> :notebook: 引用:
>
> `$remote_addr`:
>
> ​    client address

:thinking:那么, 可不可以直接通过修改变量`$remote_addr`, 然后通过配置`deny`来实现? 如下:

```nginx
proxy_set_header   X-Forwarded-For  $remote_addr;

allow 192.168.14.0/24;
allow 192.168.15.0/24;
deny all;
```

**答案是**: 不可以.



**解释如下:**

关于`$remote_addr`:

是nginx与客户端进行TCP连接过程中，获得的客户端真实地址. Remote Address 无法伪造，因为建立 TCP 连接需要三次握手，如果伪造了源 IP，无法建立 TCP 连接，更不会有后面的 HTTP 请求

remote_addr代表客户端的IP，但它的值不是由客户端提供的，而是服务端根据客户端的ip指定的，当你的浏览器访问某个网站时，假设中间没有任何代理，那么网站的web服务器（Nginx，Apache等）就会把remote_addr设为你的机器IP，如果你用了某个代理(其实F5就是个反向代理)，那么你的浏览器会先访问这个代理，然后再由这个代理转发到网站，这样web服务器就会把remote_addr设为这台代理机器的IP。

但是实际场景中，我们即使有代理，也需要将`$remote_addr`设置为真实的用户IP，以便记录在日志当中，当然nginx是有这个功能，但是需要编译的时候添加--with-http_realip_module 这个模块，默认是没有安装的。(我也没有安装)



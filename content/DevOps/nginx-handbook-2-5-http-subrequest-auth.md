Title: NGINX 实战手册-安全-HTTP 子请求认证
Category: DevOps
Date: 2019-06-19 20:13
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX的HTTP子请求认证功能.
Image: /images/nginx-ssl-certificate.jpg

### 2.5.1 介绍

伴随着很多不同的认证方法, NGINX通过启用自请求mid-flight 来使验证认证广泛的认证系统变得容易. HTTP认证请求模块可以启用如LDAP或自定义认证微服务的认证系统. 在请求被执行之前, 认证机制会代理该请求到认证服务. 在这个代理中, 通过NGINX的能力可以操纵需要身份验证服务的请求。因此,它非常灵活。

### 2.5.2 认证子请求

#### 问题

你有一个第三方的认证系统, 请求认证需要用到这个系统.

#### 解决方案

使用`http_auth_request_module`在请求执行前, 让请求到对应的认证服务来进行验证:

```conf
location /private/ {
  auth_request /auth;
  auth_request_set $auth_status $upstream_status;
}

location = /auth {
  internal;
  proxy_pass http://auth-server;
  proxy_pass_request_body off;
  proxy_set_header Content-length "";
  proxy_set_header X-Original-URI $request_uri;
}
```

`auth_request`指令使用必须是local internal location的URI参数. `auth_request_set`指令允许你从认证自请求来设置变量.

#### 讨论

`http_auth_request_module`允许对每个NGINX处理的请求做认证. 在响应原服务之前, 会生成一个子请求, 来决定这个请求是否可以访问它请求的资源.  整个请求会被代理到自请求块 location. 通过自请求的状态码来确定是否可以访问资源. 如果自请求返回200 HTTP 状态码, 认证成功, 请求被响应. 如果返回HTTP 401或403, 会向原请求返回同样的代码.

如果你的认证服务不需要请求body, 你可以抛弃掉请求body, 通过`proxy_pass_reqeust_body`指令(如上例子所示). 这会减少请求size和时间. 因为请求体被忽略, `Content-Length` header可以设为空字符串. 如果你的认证服务需要直到原请求的URI, 你可以把这个值放到一个自定义的header, 让你的认证服务来检查和验证. 如果从子请求到认证服务见你想要保留一些东西, 你可以使用  `auth_request_set`指令来创建相应数据之外新的变量.

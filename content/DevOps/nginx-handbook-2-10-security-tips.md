Title: NGINX 实战手册-安全-实用安全技巧
Category: DevOps
Date: 2019-06-19 20:24
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX的一些实用安全技巧.
Image: /images/nginx-ssl-certificate.jpg

## 2.10 实用安全技巧

### 2.10.0 介绍

安全是分层的, 就像一个洋葱, 你的安全模型确实要被多层加固. 在这部分, 我们介绍许多不同的方法来确保web应用程序NGINX和NGINX Plus. 很多的这些安全方法可以用来加固安全. 下面是一些实用的安全提示,以确保您的用户在使用HTTPS和告诉NGINX满足一个或多个安全方法。

### 2.10.1 HTTPS 重定向

#### 问题

你需要重定向未加密的请求到HTTPS.

#### 解决方案

使用`rewrite`来发送所有HTTP流量到HTTPS:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 301 https://$host$request_uri;
}
```

这个配置监听所有hostname的IPv4和IPv6的80端口作为默认的server. `return`声明返回301永久重定向到同样的host和请求URI的HTTPS上.

#### 讨论

总是把适当的请求重定向到HTTPS是非常重要的. 你可能会发现你不需要重定向所有的请求, 而是在客户端和server之间传输敏感信息的那些请求. 在本例中, 你可能想要把`return`声明放到特定的location里, 如`/login`.

### 2.10.2 重定向SSL/TLS在NGINX之前已经结束的到HTTPS

#### 问题

你需要重定向到HTTPS, 然而, 在NGINX之前, 你已经结束了SSL/TLS.

#### 解决方案

使用标准的`HTTP_X_Forwarded_Proto` 头来决定是否你需要进行重定向:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    if ($http_x_forwarded_proto = 'http') {
        return 301 https://$host$request_uri;
    }
}
```

这个配置和HTTPS重定向很像. 但是, 在这个配置中, 只有头`X_Forwarded_Proto`等于HTTP才会重定向.

#### 讨论

这是一个在NGINX之前就结束了SSL/TLS的常见案例. 你可能要这么做的一个原因是节省计算开销. 但是, 你需要确保每个请求都是HTTPS, 但是结束了SSL/TLS的层没有重定向的能力. 但是, 可以设置代理头部. 这个配置可以在Amazon Web Services Elastic Load Balancer上工作, 因为这个如果没有额外的花钱的话就会卸载掉SSL/TLS. 这是一个方便的技巧以确保你的HTTP流量是安全的。

### 2.10.3 满足任意数量的安全方法

#### 问题

你需要提供多种方式来传输安全到一个不公开的站点.

#### 解决方案

使用`satisfy`指令来说明你想要使用任意数量的安全方法:

```nginx
location / {
    satisfy any;
    allow 192.168.1.0/24;
    deny  all;
    auth_basic           "closed site";
    auth_basic_user_file conf/htpasswd;
}
```

该配置告诉NGINX用户请求`location /`需要满足其中的一个安全方法: 或者该请求需要来自*192.168.1.0/24* CIDR block, 或者能够提供在可以在`conf/htpasswd`中找到的用户名密码. `satisfy`指令有2个选项: `any`或`all`

#### 讨论

`satifsy`指令是一个提供多种认证的很好的方式. 通过指定`any`给`satisfy`指令, 用户必须满足其中一个安全. 指定`all`给`satisfy`指令, 用户必须满足所有的安全认证. 该指令可以和2.1的`http_access_module`结合, 2.4的`http_auth_basic_module`, 2.5的`http_auth_request_module`, 2.7的`http_auth_jwt_module`. 只有各个层都安全, 才是真正的安全. `satisfy`指令会帮助你为这个location或server实现需要的深度安全规则.

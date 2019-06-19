Title: NGINX 实战手册-安全-限制使用
Category: DevOps
Date: 2019-06-19 20:05
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX限制使用.
Image: /images/nginx-ssl-certificate.jpg

## 2.2 限制使用

### 2.2.0 介绍

该章节关注于: 限制使用和滥用, 连接数, 请求服务速率, 带宽使用量. 区分开连接和请求是很重要的: 连接(TCP连接)是网络层, 在这层上, 请求被执行, 因此两者并不一样.

在HTTP/1和HTTP/1.1中, 一个连接请求只能使用一次; 而在HTTP/2中, 多个请求可以使用同一个TCP连接.

### 2.2.1 限制连接

#### 问题

你需要基于预定义的key来限制连接数, 比如key是客户端IP地址.

#### 解决方案

创建一个共享内存区域来存放连接metrics, 并使用`limit_conn` 指令来限制打开的连接数:

```nginx
http {
  limit_conn_zone $binary_remote_addr zone=limitbyaddr:10m;
  limit_conn_status 429;
  ...
  server {
    ...
      limit_conn limitbyaddr 40;
    ...
  }
}
```

> :heavy_check_mark:  
>
> 429: Too Many Requests
>
> 预定义的key用的是:二进制格式的客户端IP地址.

#### 讨论

使用IP地址, 就像上个例子中那样, 如果很多用户都在同一个网络来自同一个IP可能很危险, 比如用的是一个NAT(网络地址转换). 整个组都会被限制. `limit_conn_zone`指令只适用于HTTP块. 可以利用在HTTP块中的NGINX的任何变量来构建一个字符串来限制. 利用变量可以在应用级别识别具体的用户, 像是session cookie, 基于使用案例可能是一个更干净的解决方案. `limit_conn`和`limit_conn_status`指令在HTTP, server, 和location块中都能用. `limit_conn_status`默认是503, 服务不可用. 429会更合适, 因为500界别的服务不可用意味着错误.

### 2.2.2 限制速率

#### 问题

你需要基于预定义的key来限制请求速率, 比如客户端IP地址.

#### 解决方案

利用速率限制模块来限制:

```nginx
http {
  limit_req_zone $binary_remote_addr zone=limitbyaddr:10m rate=1r/s;
  limit_req_status 429;
  ...;
  server {
    ...
      limit_req zone=limitbyaddr burst=10 nodelay;
    ...;
  }
}
```

这个zone用关键字参数设置了速率. `limit_req`指令有2个关键字参数: `zone`和`burst`. 当给定zone的请求速率超出了, 请求会延迟直到达到他们的最大burst size, 这个由`burst`关键字参数提供. 默认`burst`关键字参数为0. `limit_req`也有第三个可选的参数, `nodelay`. 这个参数允许客户端在被限制之前使用它的`burst`而不用延迟. `limit_req_status` 和`limit_req` 可以用在HTTP, server, 和location. `limit_req_zone`只适用于HTTP块.

#### 讨论

速率限制模块在组织恶意请求, 同时仍为每个人提供一定质量的服务时非常有用. 有很多限制请求速率的原因, 其中之一就是安全. 你可以通过在你的登陆页面设置非常严格的限制来防止恶意攻击. 你可以通过设置对所有请求的完善的限制来阻止恶意用户尝试对你的应用使用拒绝式服务攻击或浪费资源的计划. 速率限制模块的配置和2.2.1中的很类似. 速率可以被设置为每秒多少请求或每分钟多少请求. 当超过限制, 会记录事件日志. 例子中没有提到这个指令`limit_req_log_level` , 默认是`error`, 但是也可以设置为`info` , `notice`, `warn`.

### 2.2.3 限制带宽

> 待补充

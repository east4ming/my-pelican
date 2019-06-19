Title: NGINX 实战手册-安全-加密
Category: DevOps
Date: 2019-06-19 20:08
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX进行加密.
Image: /images/nginx-ssl-certificate.jpg

## 2.3 加密

### 2.3.0 介绍

网络是个很可怕的地方, 但不需太过担心. 加密传输信息变得越来越容易, 越来越唾手可得, 因为签名证书在*Let's Encrypt*和*Amazon Web Services*变得越来越便宜. 二者都提供有限用途的免费证书. 在本章, 我们将讨论如何确保NGINX和客户端之间, 以及NGINX和upstream之间的信息安全.

### 2.3.1 客户端加密

#### 问题

需要加密NGINX和客户端之间的流量.

#### 解决方案

使用SSL模块, 如`ngx_http_ssl_module`或`ngx_stream_ssl_module`来加密流量.

```nginx.conf
http { # All directives used below are also valid in stream
    server {
        listen 8083 ssl;
        ssl_protocols       TLSv1.2; # 协议
        ssl_ciphers         AES128-SHA:AES256-SHA; # 密码套件
        ssl_certificate     /usr/local/nginx/conf/cert.pem; # 证书
        ssl_certificate_key /usr/local/nginx/conf/cert.key; # 密钥
        ssl_session_cache   shared:SSL:10m; # ssl会话缓存
        ssl_session_timeout 10m; # ssl会话超时
    }
}
```

#### 讨论

- 不要使用SSL(Secure Socket Layer)协议, 1 - 3版都被认为不安全
- TLS是默认的协议(Transport Layer Security), TLS还算安全.
- 当使用签名证书, 你需要把证书和证书认证链连接到一块. 你的证书应该在证书链文件的上方.
- **SSL会话缓存, 缓存后无需negotiate 版本和密码套件, 可以提升性能.**

### 2.3.2 Upstream 加密

#### 问题

为了合规, 或者你的upstream在你的安全网络之外, 你需要加密NGINX和upstream之间的流量.

#### 解决方案

使用HTTP 代理模块的SSL指令

```nginx.conf
location / {
    proxy_pass https://upstream.example.com;
    proxy_ssl_verify on;
    proxy_ssl_verify_depth 2;
    proxy_ssl_protocols TLSv1.2;
}
```

配置的指令确保NGINX在upsteam上验证证书和证书链2层认证深度是合法的. 默认NGINX**不验证**upstream证书, 接收所有TLS版本.

#### 讨论

- 如果要加密upstream 流量, 你至少应该开启验证.
- 其他可用指令, 如`proxy_ssl_certificate`和`proxy_ssl_certificate_key`, 允许你锁定upstream加密以增强安全性.

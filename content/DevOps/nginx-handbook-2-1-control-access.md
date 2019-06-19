Title: NGINX 实战手册-安全-访问控制
Category: DevOps
Date: 2019-06-19 20:00
Tags: nginx, 安全, 译文, 最佳实践
Summary: NGINX 实战手册系列文章的安全部分. 本文专注于如何使用NGINX进行访问控制.
Image: /images/nginx-ssl-certificate.jpg

## 2.1.1 介绍

控制你的web应用或你的web应用的子网的访问是很重要的业务. 在NGINX中, 访问控制有多种形式, 像是在网络层拒绝掉, 基于认证策略的允许, 或 HTTP指令浏览器如何响应. 本章我们将讨论基于网络属性, 认证和如何防止*跨域资源共享(Cross-Origin Resource Sharing(CORS))*的访问控制.

## 2.1.2 基于IP地址的访问

### 问题

你需要基于客户端的IP地址的控制.

### 解决方案

使用HTTP访问模块来控制对受保护资源的访问:

```conf
location / {
  deny 10.0.0.1;
  allow 10.0.0.0/20;
  allow 2001:0db8::/32;
  deny all;
}
```

在HTTP, server, 和location上下文中, `allow`和`deny`指令提供对给出的client, IP, CIDR range, Unix socket, 或all 关键字的允许和禁止访问的能力. 规则被依次检查, 直到发现匹配的地址.

### 讨论

保护在互联网上的有价值的资源和服务必须在对应的层上做. NGINX提供对其中一些层的能力. `deny` 指令组织访问给定的上下文, `allow`指令可以用于限制访问. 你可以使用IP地址, IPv4或IPv6, CIDR block ranges, 关键字`all`, 和Unix socket. 通常要保护某个资源, 应该允许特定区域的内网IP地址, 并拒绝所有.

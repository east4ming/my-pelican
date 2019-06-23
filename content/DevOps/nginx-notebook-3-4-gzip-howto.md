Title: NGINX 学习笔记-Gzip压缩-Gzip压缩功能的使用
Category: DevOps
Date: 2019-06-23 17:08
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的NGINX服务器Gzip压缩部分. 本文介绍NGINX Gzip压缩功能的使用.
Image: /images/nginx-logo.png

## 4 Gzip压缩功能的使用

### Gzip压缩功能综合配置示例

```nginx
http {
    gzip on;
    gzip_min_length 1024;
    gzip_buffers 32 4k;
    gzip_comp_level 2;
    gzip_types text/plain application/x-javascript text/css application/xml;
    gzip_vary on;
    gunzip_static on;
}
```

### Gzip 压缩功能与IE6浏览器运行脚本的兼容问题

```nginx
gzip_disable "MSIE [1-6]\.";
```

### Nginx与其他服务器交互时产生的Gzip压缩功能相关问题

两类问题:

1. 多层服务器同时开启Gzip压缩功能导致;
2. 多层服务器之间对Gzip压缩功能支持能力不同导致.

Nginx与后端服务器(如Tomcat)同时开启Gzip压缩功能对JavaScript脚本进行压缩, 在大多数浏览器中刷新页面会导致脚本运行发生异常, 唯一可以运行的浏览器是Chrome.

解决办法:**对于包含多层服务器的系统来说, Nginx服务器作为前端服务器如果开启了Gzip压缩功能, 后端服务器最好就不要再开启了.**

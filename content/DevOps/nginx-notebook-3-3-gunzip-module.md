Title: NGINX 学习笔记-Gzip压缩-`ngx_http_gunzip_module`
Category: DevOps
Date: 2019-06-23 17:08
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的NGINX服务器Gzip压缩部分. 本文介绍NGINX `ngx_http_gunzip_module` 模块.
Image: /images/nginx-logo.png

## 3 ngx_http_gunzip_module

如果客户端本身不支持解压Gzip, 就需要Nginx服务器在向其发送数据前先将该数据解压. 这些压缩数据可能来自于后端服务器压缩产生或Nginx服务器预压缩产生.

该模块不是默认构建的，应该使用 `--with-http_gunzip_module` 配置参数启用。

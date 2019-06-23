Title: NGINX 学习笔记-高级配置-与网络连接相关的指令
Category: DevOps
Date: 2019-06-23 16:27
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的NGINX服务器高级配置部分. 本文介绍NGINX 与网络连接相关的指令.
Image: /images/nginx-logo.png

## 3 与网络连接相关的配置指令

1. keepalive_timeout

   `keepalive_timeout 60 50;`

   Nginx服务器与客户端连接保持活动的时间为60s, 60s后服务器与客户端断开连接; 使用Keep-Alive 消息头保持与客户端某些浏览器(如火狐)的连接时间为50s, 50s后浏览器主动与服务器断开连接.

2. send_timeout

   设置Nginx服务器响应客户端的超时时间, 这个超时时间仅针对两个客户端和服务器之间建立连接后, 某次活动之间的时间. 如果这个时间后客户端没有任何活动, Nginx服务器将会关闭连接. 此指令的设置需要考虑服务器访问数量和网络状况等方面.

3. client_header_buffer_size

   设置Nginx服务器允许的客户端请求头部的缓冲区大小, 默认为1KB. 此指令的赋值可以根据系统分页大小来设置. 分页大小可以通过下列命令获得:

   `getconf PAGESIZE` (一般为4k)

   > Nginx 400类错误, 有很大一部分情况是客户端的请求头部过大造成的. 请求头部过大, 通常是客户端cookie中写入了较大的值引起的.
   >
   > 适当增大此指令的赋值, 可以改善该问题.

   推荐配置:(与系统分页大小相同)

   `client_header_buffer_size 4k;`

4. multi_accept

   Nginx服务器是否尽可能多地接收客户端的网络连接请求. 默认为off.

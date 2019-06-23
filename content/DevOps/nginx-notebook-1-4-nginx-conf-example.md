Title: NGINX 学习笔记-安装部署-服务器基础配置示例
Category: DevOps
Date: 2019-06-23 16:07
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的安装部署部分. 本文介绍NGINX 服务器的基础配置示例.
Image: /images/nginx-logo.png

## 4 Nginx服务器基础配置示例

```nginx
#### 全局块 开始 #####
user nobody nobody;    # 配置允许运行Nginx服务器的用户和用户组

worker_processes 4;    # 配置允许Nginx进程生成的worker process数

error_log logs/error.log;    # Nginx错误日志输出目录

pid nginx.pid;    # 配置Nginx服务器运行时的pid文件存放路径和名称
#### 全局块 结束 #####

#### events块 开始 ####
events
{
    user epoll;    # 配置事件驱动模型
    worker_connections 1024;    # 配置最大连接数
}
#### events块 结束 ####

#### http块 开始 ####
http {
    include mime.types;   # 定义MIME-Type

    default_type application/octet-stream;

    sendfile on;    # 配置允许使用sendfile方式传输

    keepalive_timeout 65;    # 配置连接超时时间

    log_format access.log '$remote_addr-[$time_local]-"$request"-"$http_user_agent"';    # 配置请求处理日志的格式

    #### server块 开始 ####
    ## 配置虚拟主机myServer1
    server {
        listen 8081;    # 配置监听端口和主机名称
        server_name myServer1;
        access_log /myweb/server1/log/access.log;    # 配置请求处理日志存放路径
        error_page 404 /404.html;    # 配置错误页面
        location /server1/location1 {    # 配置处理/server1/location1请求的location
            root /myweb;
            index index.svr1-loc1.htm;
        }

        location /server1/location2 {    # 配置处理/server1/location1请求的location
            root /myweb;
            index index.svr1-loc2.htm;
        }
    }

    server {    ## 配置虚拟主机 myServer2
        listen 8082;
        server_name 192.168.1.3;
        access_log /myweb/server2/log/access.log;
        error_page 404 /404.html;
        location /server2/location1 {
            root /myweb;
            index index.svr2-loc1.htm;
        }
        location /svr2/loc2 {
          alias /myweb/server2/location2;    # 对location的URI进行更改
          index index.svr2-loc2.htm;
        }
        location = /404.html {    # 配置错误页面转向
            root /myweb/;
            index 404.html;
        }
    }
    #### server 块 结束 ####
}
#### http块 结束 ####
```

配置后的目录结构

```
myweb
    404.html
    server1
        location1
            index.svr1-loc1.htm
        location2
            index.svr1-loc2.htm
        log
            access.log
    server2
        location1
            index.svr2-loc1.htm
        location2
            index.svr2-loc2.htm
        log
            access.log
```

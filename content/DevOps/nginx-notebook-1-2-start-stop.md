Title: NGINX 学习笔记-安装部署-启停控制
Category: DevOps
Date: 2019-06-23 15:25
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的安装部署部分. 本文介绍NGINX 启停命令.
Image: /images/nginx-logo.png

## Nginx启停控制

- `nginx -t` 检查Nginx服务器配置文件是否有语法错误
- `nginx` 启动
- `nginx -s stop` 停止
- `nginx -s reload`  或 ```kill HUP `/Nginx/logs/nginx.pid` ```  平滑重启
- 平滑升级: 先执行```kill USR2 `/Nginx/logs/nginx.pid` ```实现Nginx服务的平滑升级; 再使用```kill WINCH `/Nginx/logs/nginx.pid` ```平滑停止旧服务信号

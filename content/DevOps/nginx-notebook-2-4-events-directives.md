Title: NGINX 学习笔记-高级配置-事件驱动模型相关的配置指令
Category: DevOps
Date: 2019-06-23 16:33
Tags: nginx, 最佳实践
Summary: NGINX 学习笔记系列文章的NGINX服务器高级配置部分. 本文介绍NGINX 事件驱动模型相关的配置指令.
Image: /images/nginx-logo.png

## 4 事件驱动模型相关的配置指令

1. `use`(指定事件驱动模型)
2. `worker_connections`

   用于设置Nginx服务器的**每个工作进程**允许同时连接客户端的最大数量(包括前端用户连接也包括其他连接)

   Nginx服务器允许同时连接的客户端最大数量 `Client = worker_processes * worker_connections / 2`

3. `worker_rlimit_sigpending`

   事件驱动模型rtsig可以保存的最大信号数.

4. `devpoll_changes` `devpoll_events`

   用于设置在`/dev/poll`事件驱动模式下Nginx服务器与内核之间传递事件的数量.前者设置传递给内核的事件数量, 后者设置从内核获取的事件数量.

   默认值为32

5. `kqueue_changes` 和 `kqueue_events`

   kqueue事件模型下. 默认值均为512

6. `epoll_events`

   epoll事件模型下, 从Nginx到内核, 从内核到Nginx相等. 默认值为512.

7. `rtsig_signo`

   rtsig模式. 默认第一个信号设置为SIGRTMIN+10

8. `rtsig_overflow_*`

> :notebook:备注:
>
> 现在的Linux发行版一般推荐使用`epoll`事件驱动模型
